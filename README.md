# SafeStreak

> "If you know the enemy and know yourself, you need not fear the result of a hundred battles. *-Sun Tzu*

free and open source bedwars stats overlay for lunar client 1.8 to help you keep your winstreak.

tested on linux and windows, macos will *probably* work as well (I don't have a mac on hand to test with)

## installing/updating on windows
paste into start menu and hit enter:

```
powershell "Write-Output (Invoke-WebRequest https://raw.githubusercontent.com/An0nDev/safestreak/master/install_windows.ps1 -UseBasicParsing).Content" | powershell -noprofile -
```

you can then double-click on `run.py` in your documents folder --> safestreak-master

(read `install_windows.ps1` to see what the installer does)

## data location
all data is stored in `<home folder>/.safestreak` (eg `C:\Users\USER\.safestreak` on Windows and `~/.safestreak` on macOS/Linux)

if you are having issues, try deleting the folder before opening an issue in the repo

## other info
- the button to the right of the stats lets you pin and unpin individuals
- your username is automatically added as a pin, change your username in the settings
- running /p list auto-adds leader/members as pins
- running /p warp auto-clears non-pins
- join and quit messages from the bedwars lobby will add and remove individuals unless pinned
- running /who will add all members in the game (auto-who recommended)
- reading list and warp messages from parties with more than two people is not supported (i just need to test this)

python requirements are `requests` for mojang/hypixel api and `watchdog` for log file watching (i think thats it)

these are automatically installed by the windows installer, on linux you can probably handle it on your own. macos is not officially supported

## supporters
cool mc people are:
- d9f9d8ea4f054a5fac211b51d9e448ad 
- 3712b4872b2346c38d6774fa3d27b58f
- 518d492516a447b4a56213d5465f0eba
- 06b57734e6eb4ee3a7b53492d5fbb5e6
- 163fe2178bc04749a50c17e0ae51c4a5