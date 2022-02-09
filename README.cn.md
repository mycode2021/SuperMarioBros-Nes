[English](./README.md) | 简体中文 

# 项目说明

这是一个超级马里奥兄弟环境用于openAI's retro, 这个项目用于扩展官方原生环境。

# 测试环境

## 1. 系统依赖库

你需要使用openAI的gym-retro-integration工具提取rom文件和sha文件并与SuperMarioBros-Nes目录合并成一个完整的环境。
```bash
mv "python's library directory"/site-packages/retro/data/stable/SuperMarioBros-Nes \
  "python's library directory"/site-packages/retro/data/stable/SuperMarioBros-Nes.bak
```
```bash
cp -Rp SuperMarioBros-Nes "python's library directory"/site-packages/retro/data/stable/SuperMarioBros-Nes
```

###### :point_right: **提示: gym-retro-integration工具linux下你可以通过gym-retro源码编译获得。ROM文件也许你可以在 https://romhustler.org 找到。**

# 工具说明

**例如:**
```bash
python test.py --state Level2-1 --from_model Level2-1
```

**回放:**
```bash
python -m retro.scripts.playback_movie SuperMarioBros-Nes-Level2-1-000000.bk2
```
