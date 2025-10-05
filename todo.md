# TODO

## 项目：Nekro Agent Toolkit NixOS Demo 镜像自动化构建

### 当前开发内容

1. **自动化 Demo 镜像构建流程**
   - 使用 GitHub Actions 自动构建 Nekro Agent Toolkit 的 NixOS demo 虚拟机镜像。
   - 镜像仅用于演示和体验，方便其他用户导入后直接试用 toolkit。
   - 通过 nixos-generators flakes 从 GitHub 仓库拉取配置，最大化兼容性。
   - 支持 QCOW2 镜像自动生成，并用 qemu-img 转换为 VMDK 格式。
   - 镜像文件自动打包为 zip，便于分发和下载。

2. **CI/CD 兼容性优化**
   - 解决 flakes lock 文件写入权限问题，所有相关命令加 --no-write-lock-file。
   - 保证 workflow 在 GitHub Actions 环境下稳定运行，无需本地 flakes 依赖。

3. **配置文件规范化**
   - flake.nix 只定义 NixOS 配置，所有依赖由官方 flakes 拉取。
   - 镜像构建入口统一为 GitHub 仓库 flakes，避免本地依赖不一致。

### 重要说明

- 当前 demo 镜像仅用于 Nekro Agent Toolkit 的体验和演示。
- 镜像不包含完整的 NixOS 启动引导（bootloader），无法直接作为独立系统启动。
- 仅适合导入到虚拟机环境进行功能体验，不适合生产或持久化部署。



---

