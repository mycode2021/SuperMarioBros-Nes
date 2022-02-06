# Description

This is a Super Mario environment for openai retro.

# Environment

You need to use openAI's gym-retro-integration gets rom files and sha files and merge with the SuperMarioBros-Nes catalog to form a complete environment.
```bash
mv "python's library directory"/site-packages/retro/data/stable/SuperMarioBros-Nes \
  "python's library directory"/site-packages/retro/data/stable/SuperMarioBros-Nes.bak
```
```bash
cp -Rp retro/data/experimental/SuperMarioBros-Nes \
  "python's library directory"/site-packages/retro/data/stable
```

###### :point_right: **Tips: The gym-retro-Integration tool is available under linux through the gym-retro source compilation. ROM file maybe you can find from https://romhustler.org.**

# Toolkit

**For example:**
```bash
python test.py --game SuperMarioBros-Nes --state Level8-1 --from_model Level8-1
```
