# yt-dlp-ytdlp-jsc

A yt-dlp plugin that provides a JS Challenge Provider using the [ytdlp-jsc](https://pypi.org/project/ytdlp-jsc/) library to solve YouTube N/Sig challenges.

## Requirements

1. Python 3.10+
2. yt-dlp `2025.11.12` or above
3. [ytdlp-jsc](https://pypi.org/project/ytdlp-jsc/) library

## Installing

### pip/pipx

If yt-dlp is installed through `pip` or `pipx`, you can install the plugin with:

```bash
pipx inject yt-dlp yt-dlp-ytdlp-jsc
```

or

```bash
python3 -m pip install -U yt-dlp-ytdlp-jsc
```

### git
```bash
git clone https://github.com/ahaoboy/ytdlp-jsc-plugin.git --depth=1 ~/.yt-dlp/plugins/ytdlp-jsc-plugin
```

### Manual

1. Go to the [latest release](https://github.com/grqz/yt-dlp-ytdlp-jsc/releases/latest)
2. Download `yt-dlp-ytdlp-jsc.zip` to one of the [yt-dlp plugin locations](https://github.com/yt-dlp/yt-dlp#installing-plugins):

   - User Plugins
     - `${XDG_CONFIG_HOME}/yt-dlp/plugins`
     - `~/.yt-dlp/plugins/`

   - System Plugins
     - `/etc/yt-dlp/plugins/`
     - `/etc/yt-dlp-plugins/`

   - Executable location
     - Binary: where `<root-dir>/yt-dlp`, `<root-dir>/yt-dlp-plugins/`

For more locations and methods, see [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins)

## Verifying Installation

If installed correctly, you should see the provider's version in `yt-dlp -v` output:

```
[debug] [youtube] [jsc] JS Challenge Providers: ..., ytdlp-jsc-0.1.0 (external), ...
```

## Debugging

Use `-v --extractor-args "youtube:jsc_trace=true"` to enable JS Challenge debug output.

## Related

- [yt-dlp JS Challenge Provider Framework](https://github.com/yt-dlp/yt-dlp/wiki)
- [ytdlp-jsc](https://pypi.org/project/ytdlp-jsc/)
