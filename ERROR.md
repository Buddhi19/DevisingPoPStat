# If you are encountering errors due to Windows-style line endings (CRLF),try followings.

**VS Code**
1. Open the file in VS Code.
2. In the bottom-right corner, click on the text that says `CRLF`.
3. Select `LF` from the menu.
4. Save the file.

**Notepad++**
1. Open the file in Notepad++.
2. Go to `Edit` > `EOL Conversion` > `Unix (LF)`.
3. Save the file.

**If you are using LINUX**
1. Install dos2unix
    ```sh
    sudo apt-get install dos2unix
2. Run the command
   ```sh
   dos2unix ./setup_environment.sh
   ```

**If you are using WSL**
1. Run the command
    ```sh
    sed -i 's/\r$//' ./setup_environment.sh
    ```