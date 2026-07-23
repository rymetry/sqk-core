# 手法選択ポインタ表（FMEA / FTA / STPA / STRIDE）

## 位置づけ

本ファイルは `risk-analysis` スキルの「手順2: 手法選択とその理由の記録」
（[../SKILL.md](../SKILL.md)）で参照する早見表である。各手法の解説・比較・
限界は docs/ 側の該当節が正典であり、本ファイルはそこへのポインタのみを
提供する。新規の解説は書かない。

## 対応表

| 手法 | 適する状況（1文要約） | 出典 |
| --- | --- | --- |
| FMEA / FMECA | ハードウェア部品・製造工程・詳細設計など、単一コンポーネントの故障モードをボトムアップで列挙したいとき | [domain-specific-quality-and-safety-standards.md §2](../../../docs/governance-compliance/domain-specific-quality-and-safety-standards.md#2-hazard-analysis-の手法) |
| FTA | 望ましくない頂上事象が既に特定できていて、そこに至る組合せ故障の論理構造を分解・定量評価したいとき | [domain-specific-quality-and-safety-standards.md §2](../../../docs/governance-compliance/domain-specific-quality-and-safety-standards.md#2-hazard-analysis-の手法) |
| STPA | ソフトウェア・自動化・人間の関与が支配的で、コンポーネントが正常でも相互作用や要求欠落から起きる事故を早期（要求段階）に捉えたいとき | [domain-specific-quality-and-safety-standards.md §2](../../../docs/governance-compliance/domain-specific-quality-and-safety-standards.md#2-hazard-analysis-の手法) |
| STRIDE | データフロー図上の信頼境界をまたぐ要素に対して、なりすまし・改ざん・否認・情報漏えい・DoS・権限昇格などセキュリティ脅威を体系的に洗い出したいとき | [secure-development-and-supply-chain.md §4.1](../../../docs/secure-development/secure-development-and-supply-chain.md#41-stride) |

## 補足

- ハードウェア故障起因が支配的な場合は FMEA/FMECA と FTA を組み合わせるのが定番（出典: 上表 domain-specific-quality-and-safety-standards.md §2 の「実務上の使い分けの目安」）。
- プロセス逸脱（化学・製薬等）が支配的な場合は HAZOP が定番だが、本スキルの対象（プロダクト・ソフトウェアリスク）では優先度は相対的に低い。詳細は同節を参照。
- セキュリティ・コンプライアンス領域の一般的なリスク評価の枠組み（ISO 31000 等）は [software-quality-management-practical-reference.md](../../../docs/quality-management/software-quality-management-practical-reference.md#リスクコンプライアンスセキュリティ品質) 経由で参照する。
- 規制ドメイン（安全・医療・金融等）に該当する場合、影響度判定の基準自体が規格で規定されることがある。ドメイン判定の手順は [domain-specific-quality-and-safety-standards.md §9](../../../docs/governance-compliance/domain-specific-quality-and-safety-standards.md) を参照。
