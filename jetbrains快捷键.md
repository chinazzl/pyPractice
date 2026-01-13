好的，JetBrains 全家桶（IntelliJ IDEA, PyCharm, WebStorm, GoLand, CLion, Rider 等）的快捷键设计得非常一致，学会一套基本可以通用。

这是一个非常全面且经过分类的 JetBrains 快捷键指南，分为 **【必会神技】** 和 **【常用分类】** 两部分。快捷键格式为 `Windows/Linux | macOS`。

---

### 【一、必会神技 (改变你使用方式的快捷键)】

这几个快捷键是 JetBrains 的精髓，能极大地提升效率。

| 功能描述 | Windows / Linux | macOS | 备注 |
| :--- | :--- | :--- | :--- |
| **万能搜索 (Find Action)** | `Ctrl + Shift + A` | `Cmd + Shift + A` | **第一神键！** 不记得任何快捷键时，按它，然后输入你想做的操作（如"reformat code", "git push"），它会帮你找到并执行。 |
| **全局搜索 (Search Everywhere)** | `双击 Shift` | `双击 Shift` | 搜索任何东西：类、文件、符号、设置、甚至是 Git 提交记录。 |
| **重构一切 (Refactor This)** | `Ctrl + Alt + Shift + T` | `Ctrl + T` | **第二神键！** 在代码上按此键，会弹出所有可用的重构选项（重命名、提取方法、提取变量等）。 |
| **智能代码生成 (Generate)** | `Alt + Insert` | `Cmd + N` | 快速生成构造函数、Getter/Setter、`toString()`、实现接口方法等。 |
| **快速修复/意图操作 (Show Intention Actions)** | `Alt + Enter` | `Alt + Enter` | **第三神键！** 任何有波浪线、黄色警告的地方，按此键 IDE 就会给你修复建议。也可用于快速创建测试、导入包等。|

---

### 【二、常用快捷键分类】

#### 1. 编辑 (Editing)

| 功能描述 | Windows / Linux | macOS |
| :--- | :--- | :--- |
| 复制当前行/选中块 | `Ctrl + D` | `Cmd + D` |
| 删除当前行 | `Ctrl + Y` | `Cmd + Delete` |
| 上/下移动行 | `Alt + Shift + ↑/↓` | `Alt + Shift + ↑/↓` |
| 智能选择扩展/收缩 | `Ctrl + W` / `Ctrl + Shift + W` | `Alt + ↑` / `Alt + ↓` |
| 格式化代码 | `Ctrl + Alt + L` | `Cmd + Alt + L` |
| 注释/取消注释 (行) | `Ctrl + /` | `Cmd + /` |
| 注释/取消注释 (块) | `Ctrl + Shift + /` | `Cmd + Alt + /` |
| 智能补全 | `Ctrl + Shift + Space` | `Ctrl + Shift + Space` |
| 基本补全 | `Ctrl + Space` | `Ctrl + Space` |
| 显示快速文档 | `Ctrl + Q` | `F1` (新版也可用 `Ctrl + J`) |

#### 2. 查找与导航 (Search & Navigation)

| 功能描述 | Windows / Linux | macOS |
| :--- | :--- | :--- |
| 查找类 | `Ctrl + N` | `Cmd + O` |
| 查找文件 | `Ctrl + Shift + N` | `Cmd + Shift + O` |
| 查找符号 (方法/变量) | `Ctrl + Alt + Shift + N` | `Cmd + Alt + O` |
| **跳转到定义/声明处** | `Ctrl + B` 或 `Ctrl + 左键点击` | `Cmd + B` 或 `Cmd + 左键点击`|
| **查看用法 (Find Usages)** | `Alt + F7` | `Alt + F7` |
| 在当前文件查找 | `Ctrl + F` | `Cmd + F` |
| 在整个项目查找 | `Ctrl + Shift + F` | `Cmd + Shift + F` |
| 在当前文件替换 | `Ctrl + R` | `Cmd + R` |
| 在整个项目替换 | `Ctrl + Shift + R` | `Cmd + Shift + R` |
| 查看最近文件 | `Ctrl + E` | `Cmd + E` |
| 在导航历史中前进/后退 | `Ctrl + Alt + ←/→` | `Cmd + [` / `Cmd + ]` |
| 跳转到指定行 | `Ctrl + G` | `Cmd + L` |

#### 3. 重构 (Refactoring)

记住 `Ctrl + Alt + Shift + T` / `Ctrl + T` 这个入口，可以找到所有重构。以下是最高频的几个。

| 功能描述 | Windows / Linux | macOS |
| :--- | :--- | :--- |
| **重命名 (Rename)** | `Shift + F6` | `Shift + F6` |
| **提取方法 (Extract Method)** | `Ctrl + Alt + M` | `Cmd + Alt + M` |
| **提取变量 (Extract Variable)** | `Ctrl + Alt + V` | `Cmd + Alt + V` |
| **提取字段/属性 (Extract Field)** | `Ctrl + Alt + F` | `Cmd + Alt + F` |
| **提取参数 (Extract Parameter)** | `Ctrl + Alt + P` | `Cmd + Alt + P` |
| **内联 (Inline)** | `Ctrl + Alt + N` | `Cmd + Alt + N` |

#### 4. 运行与调试 (Run & Debug)

| 功能描述 | Windows / Linux | macOS |
| :--- | :--- | :--- |
| 运行当前配置 | `Shift + F10` | `Ctrl + R` |
| 调试当前配置 | `Shift + F9` | `Ctrl + D` |
| 从上下文运行 (Run Context) | `Ctrl + Shift + F10` | `Ctrl + Shift + R` |
| 切换断点 | `Ctrl + F8` | `Cmd + F8` |
| 单步跳过 (Step Over) | `F8` | `F8` |
| 单步进入 (Step Into) | `F7` | `F7` |
| 智能单步进入 (Smart Step Into) | `Shift + F7` | `Shift + F7` |
| 单步跳出 (Step Out) | `Shift + F8` | `Shift + F8` |
| 继续执行 (Resume Program) | `F9` | `Cmd + Alt + R` |
| 查看所有断点 | `Ctrl + Shift + F8` | `Cmd + Shift + F8` |

#### 5. 版本控制 (VCS / Git)

| 功能描述 | Windows / Linux | macOS |
| :--- | :--- | :--- |
| 提交 (Commit) | `Ctrl + K` | `Cmd + K` |
| 推送 (Push) | `Ctrl + Shift + K` | `Cmd + Shift + K` |
| 更新项目 (Pull) | `Ctrl + T` | `Cmd + T` |
| 显示 VCS 操作弹窗 | `Alt + \`` (反引号) | `Ctrl + V` |
| 打开 Git (VCS) 工具窗 | `Alt + 9` | `Cmd + 9` |

#### 6. 窗口管理 (Window Management)

| 功能描述 | Windows / Linux | macOS |
| :--- | :--- | :--- |
| 打开/关闭项目工具窗 | `Alt + 1` | `Cmd + 1` |
| 打开/关闭终端工具窗 | `Alt + F12` | `Alt + F12` |
| 隐藏所有工具窗口 | `Ctrl + Shift + F12` | `Cmd + Shift + F12` |
| 切换到编辑器 | `Escape` | `Escape` |

---

### 【三、如何学习和自定义】

1.  **忘记了怎么办？**
    *   **首选 `Ctrl + Shift + A` (Find Action)**，输入你想做的事。
    *   在菜单栏中寻找操作，旁边通常会显示快捷键。

2.  **如何自定义？**
    *   进入 `File` -> `Settings` -> `Keymap` (Windows/Linux) 或 `IntelliJ IDEA` -> `Preferences` -> `Keymap` (macOS)。
    *   在这里你可以搜索任何一个操作，查看它当前的快捷键，或者为它分配一个新的快捷键。
    *   你还可以选择其他预设的快捷键方案，比如 `Eclipse`、`VSCode` 或 `Emacs`，方便从其他编辑器迁移过来的用户。

3.  **学习神器：`Key Promoter X` 插件**
    *   在 `Settings/Preferences` -> `Plugins` 中搜索并安装 `Key Promoter X`。
    *   当你用鼠标点击了一个有快捷键的操作时，这个插件会在右下角弹窗提示你，强制你记住快捷键。非常有效！

**建议**：不要试图一次性记住所有快捷键。从【必会神技】和【编辑】分类开始，每天有意识地使用几个，很快就会形成肌肉记忆。
