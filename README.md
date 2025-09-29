# astudy

a study

## rust 配置

```shell
# rust 安装国内源
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup

# cargo 配置国内源
vim ~/.cargo/config.toml

[source.crates-io]
registry = "https://github.com/rust-lang/crates.io-index"
replace-with = 'ustc'

[source.ustc]
registry = "git://mirrors.ustc.edu.cn/crates.io-index"

# cargo 搜索最新版本
cargo search lance --registry crates-io

# cargo 添加依赖
cargo add lance
```

## 源码软链

```shell
ln -s ../../study/agno/ agnoStudy/agno
ln -s ../../study/spark/ sparkStudy/spark
ln -s ../../study/flink/ flinkStudy/flink
```
