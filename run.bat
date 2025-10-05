@echo off
for /l %%i in (1,1,100) do (
    echo Creating file 1995%%i.txt
    echo. > %%i
)
echo Done!
pause


git pull 
git add . 
git commit -m 'm'
git push
