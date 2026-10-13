# 修改说明

发布候选版本：1.0.1-rc1。基础版本：本机 `nature-figure` 2.0.0。

本版本未声称与当前上游 main 完全一致。

## 新增

- 原生、顶层、独立可选择的 PPTX 元素交付规范。
- SVG 与 PPTX 的同源几何、文字可编辑及视觉核对要求。
- `static/core/editable-delivery.md`。
- `references/editable-ppt-workflow.md` 和 `references/editable-ppt-qa.md`。
- `scripts/audit_editability.py` 和回归测试。
- README、许可文本、来源声明和第三方内容使用边界。

## 修改

- `SKILL.md`、`manifest.yaml`：配套格式默认值、路由与版本信息。
- 继承的后端、契约及相关参考文件：仅为 PPT 制作与兼容渲染增加狭义例外，不改变科学分析语言选择。
- `references/demos.md`、`references/design-theory.md`：补充第三方许可提醒。
- 相对于本机基础版本发生改动的继承文本文件带有修改标记。素材原文件保持不变。

## 能力不变的边界

不是独立的通用 SVG 转换器；原生可编辑对象不等于与 Excel 联动的 Office 图表。结构检测不替代视觉检查、统计审核或真实 PowerPoint 交互测试。
