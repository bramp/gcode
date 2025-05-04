# Specifications for g-code

## Generic G-code Commands

```shell
curl "https://reprap.org/mediawiki/index.php?title=G-code&action=raw" | \
pandoc -f mediawiki -t markdown - > gcode.md
```

## Prusa Buddy Firmware Specific G-code Commands

```shell
curl "https://help.prusa3d.com/article/prusa-firmware-specific-g-code-commands_112173" | \
pandoc -f html -t markdown - > prusa.md
```

## Prusa Buddy Firmware Specific G-code Commands

```shell
curl "https://help.prusa3d.com/article/buddy-firmware-specific-g-code-commands_633112" | \
pandoc -f html -t markdown - > buddy.md
```
