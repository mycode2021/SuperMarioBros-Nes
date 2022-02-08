English | [简体中文](./README.cn.md)

# Description

This is a Super Mario Bros environment for openAI's retro.

# Environment

You need to use openAI's gym-retro-integration gets rom and sha files and merge with the SuperMarioBros-Nes catalog to form a complete environment.
```bash
mv "python's library directory"/site-packages/retro/data/stable/SuperMarioBros-Nes \
  "python's library directory"/site-packages/retro/data/stable/SuperMarioBros-Nes.bak
```
```bash
cp -Rp SuperMarioBros-Nes "python's library directory"/site-packages/retro/data/stable/SuperMarioBros-Nes
```

###### :point_right: **Tips: The gym-retro-Integration tool is available under linux through the gym-retro source compilation. ROM file maybe you can find from https://romhustler.org.**

# Toolkit

**For example:**
```bash
python test.py --state Level2-1 --from_model Level2-1
```

**Playback movie:**
```bash
python -m retro.scripts.playback_movie SuperMarioBros-Nes-Level2-1-000000.bk2
```
