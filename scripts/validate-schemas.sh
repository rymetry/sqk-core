#!/usr/bin/env bash
set -euo pipefail

readonly AJV_CLI_VERSION="5.0.0"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
readonly FIXTURES_ROOT="schemas/tests/fixtures"
readonly STRICT_WARNINGS_BASELINE="schemas/tests/strict-warnings-baseline.txt"

cd "${REPO_ROOT}"

tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/sqk-schema-validation.XXXXXX")"
trap 'rm -rf "${tmp_dir}"' EXIT

readonly strict_warnings_file="${tmp_dir}/strict-warnings.log"
readonly known_strict_warnings_file="${tmp_dir}/known-strict-warnings.log"
readonly new_strict_warnings_file="${tmp_dir}/new-strict-warnings.log"
readonly stale_strict_warnings_file="${tmp_dir}/stale-strict-warnings.log"
: >"${strict_warnings_file}"
: >"${known_strict_warnings_file}"
: >"${new_strict_warnings_file}"
: >"${stale_strict_warnings_file}"

compile_pass=0
compile_fail=0
fixture_pass=0
fixture_fail=0

ajv() {
  npx --yes "ajv-cli@${AJV_CLI_VERSION}" "$@"
}

print_failure_output() {
  local output_file="$1"

  if [[ -s "${output_file}" ]]; then
    sed 's/^/    /' "${output_file}"
  fi
}

compile_schema() {
  local schema="$1"
  local name output_file

  name="$(basename "${schema}" .schema.json)"
  output_file="${tmp_dir}/compile-${name}.log"

  # release-decision.schema.json uses required inside anyOf, which conflicts with
  # strictRequired. Apply this uniformly because missing required properties are
  # still caught by the invalid round-trip fixtures.
  if ajv compile --spec=draft2020 --strict=log --strict-required=false -s "${schema}" >"${output_file}" 2>&1; then
    compile_pass=$((compile_pass + 1))
    printf '  PASS %s\n' "${schema}"
  else
    compile_fail=$((compile_fail + 1))
    printf '  FAIL %s\n' "${schema}"
    print_failure_output "${output_file}"
  fi

  grep 'strict mode:' "${output_file}" >>"${strict_warnings_file}" || true
}

validate_fixture() {
  local schema="$1"
  local fixture="$2"
  local expectation="$3"
  local name output_file

  name="$(basename "${fixture}" .json)"
  output_file="${tmp_dir}/fixture-$(basename "${schema}" .schema.json)-${expectation}-${name}.log"

  if [[ "${expectation}" == "valid" ]]; then
    if ajv validate --spec=draft2020 --strict=log -s "${schema}" -d "${fixture}" >"${output_file}" 2>&1; then
      fixture_pass=$((fixture_pass + 1))
      printf '  PASS valid   %s\n' "${fixture}"
    else
      fixture_fail=$((fixture_fail + 1))
      printf '  FAIL valid   %s (fixture was rejected)\n' "${fixture}"
      print_failure_output "${output_file}"
    fi
    return
  fi

  if ajv validate --spec=draft2020 --strict=log -s "${schema}" -d "${fixture}" >"${output_file}" 2>&1; then
    fixture_fail=$((fixture_fail + 1))
    printf '  FAIL invalid %s (fixture was accepted)\n' "${fixture}"
    print_failure_output "${output_file}"
  else
    fixture_pass=$((fixture_pass + 1))
    printf '  PASS invalid %s\n' "${fixture}"
  fi
}

validate_schema_fixtures() {
  local schema="$1"
  local name fixture_dir fixture
  local -a valid_fixtures invalid_fixtures

  name="$(basename "${schema}" .schema.json)"
  fixture_dir="${FIXTURES_ROOT}/${name}"

  if [[ ! -d "${fixture_dir}" ]]; then
    fixture_fail=$((fixture_fail + 1))
    printf '  FAIL missing fixture directory: %s\n' "${fixture_dir}"
    return
  fi

  valid_fixtures=("${fixture_dir}"/valid/*.json)
  invalid_fixtures=("${fixture_dir}"/invalid/*.json)

  if (( ${#valid_fixtures[@]} == 0 )); then
    fixture_fail=$((fixture_fail + 1))
    printf '  FAIL no valid fixtures: %s/valid\n' "${fixture_dir}"
  else
    for fixture in "${valid_fixtures[@]}"; do
      validate_fixture "${schema}" "${fixture}" valid
    done
  fi

  if (( ${#invalid_fixtures[@]} == 0 )); then
    fixture_fail=$((fixture_fail + 1))
    printf '  FAIL no invalid fixtures: %s/invalid\n' "${fixture_dir}"
  else
    for fixture in "${invalid_fixtures[@]}"; do
      validate_fixture "${schema}" "${fixture}" invalid
    done
  fi
}

check_orphan_fixture_directories() {
  local fixture_dir name schema

  for fixture_dir in "${FIXTURES_ROOT}"/*; do
    [[ -d "${fixture_dir}" ]] || continue
    name="$(basename "${fixture_dir}")"
    schema="schemas/${name}.schema.json"
    if [[ ! -f "${schema}" ]]; then
      fixture_fail=$((fixture_fail + 1))
      printf '  FAIL fixture directory has no matching schema: %s\n' "${fixture_dir}"
    fi
  done
}

classify_strict_warnings() {
  local warning entry matched
  local -a baseline_entries

  baseline_entries=()
  while IFS= read -r entry || [[ -n "${entry}" ]]; do
    entry="${entry%$'\r'}"
    [[ ! "${entry}" =~ ^[[:space:]]*$ ]] || continue
    [[ "${entry}" =~ ^[[:space:]]*# ]] && continue
    baseline_entries[${#baseline_entries[@]}]="${entry}"
  done <"${STRICT_WARNINGS_BASELINE}"

  while IFS= read -r warning || [[ -n "${warning}" ]]; do
    matched=false
    for entry in "${baseline_entries[@]}"; do
      if [[ "${warning}" == *"${entry}"* ]]; then
        matched=true
        break
      fi
    done

    if [[ "${matched}" == true ]]; then
      printf '%s\n' "${warning}" >>"${known_strict_warnings_file}"
    else
      printf '%s\n' "${warning}" >>"${new_strict_warnings_file}"
    fi
  done <"${strict_warnings_file}"

  for entry in "${baseline_entries[@]}"; do
    matched=false
    while IFS= read -r warning || [[ -n "${warning}" ]]; do
      if [[ "${warning}" == *"${entry}"* ]]; then
        matched=true
        break
      fi
    done <"${strict_warnings_file}"

    if [[ "${matched}" == false ]]; then
      printf '%s\n' "${entry}" >>"${stale_strict_warnings_file}"
    fi
  done
}

shopt -s nullglob
schema_files=(schemas/*.schema.json)

printf 'Strict compile (ajv-cli@%s)\n' "${AJV_CLI_VERSION}"
for schema in "${schema_files[@]}"; do
  compile_schema "${schema}"
done

printf '\nFixture validation\n'
for schema in "${schema_files[@]}"; do
  validate_schema_fixtures "${schema}"
done
check_orphan_fixture_directories

classify_strict_warnings

strict_warning_count="$(wc -l <"${strict_warnings_file}" | tr -d '[:space:]')"
known_strict_warning_count="$(wc -l <"${known_strict_warnings_file}" | tr -d '[:space:]')"
new_strict_warning_count="$(wc -l <"${new_strict_warnings_file}" | tr -d '[:space:]')"
stale_strict_warning_count="$(wc -l <"${stale_strict_warnings_file}" | tr -d '[:space:]')"
compile_total="${#schema_files[@]}"

printf '\nSummary\n'
printf '  Compile: %d/%d passed, %d failed\n' "${compile_pass}" "${compile_total}" "${compile_fail}"
printf '  Strict warnings: known %d, new %d, stale baseline %d\n' \
  "${known_strict_warning_count}" "${new_strict_warning_count}" "${stale_strict_warning_count}"
if (( new_strict_warning_count > 0 )); then
  printf '    New warnings:\n'
  sed 's/^/      - /' "${new_strict_warnings_file}"
fi
if (( stale_strict_warning_count > 0 )); then
  printf '    Stale baseline entries:\n'
  sed 's/^/      - /' "${stale_strict_warnings_file}"
fi
printf '  Fixtures: PASS %d, FAIL %d\n' "${fixture_pass}" "${fixture_fail}"

status=0
if (( compile_fail > 0 || fixture_fail > 0 || new_strict_warning_count > 0 || stale_strict_warning_count > 0 )); then
  status=1
fi
if [[ "${AJV_STRICT_WARNINGS:-}" == "fail" ]] && (( strict_warning_count > 0 )); then
  printf '  Strict warning policy: FAIL (AJV_STRICT_WARNINGS=fail)\n'
  status=1
fi

exit "${status}"
