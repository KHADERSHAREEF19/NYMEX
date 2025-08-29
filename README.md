<html>
    <div>
        <article>
            <h1>🕵️ Nymex</h1>
            <p>
                Nymex is a simple, interactive command-line OSINT tool to check if an email address is associated with accounts on various popular websites.  
                It also includes a feature to quickly open any user's TryHackMe profile in your browser.  
            </p>
            <img src="https://your-tool-logo-link-here.png" alt="Tool Logo" width="400">
            <hr>
            <h2>🚀 Installation</h2>
            <p>
                You can install this tool by cloning the repository and setting it up.
            </p>
            <ol>
                <li>
                    <strong>Clone the repository:</strong>
                    <pre><code>https://github.com/KHADERSHAREEF19/nymex.git</code></pre>
                </li>
                <li>
                    <strong>Navigate into the directory:</strong>
                    <pre><code>cd Nymex</code></pre>
                </li>
                <li>
                    <strong>Install the required libraries:</strong>
                    <pre><code>pip install httpx termcolor</code></pre>
                </li>
                <li>
                    <strong>Run the installer (optional, if you want global usage):</strong>
                    <pre><code>sudo bash install.sh</code></pre>
                </li>
            </ol>
            <!-- Usage Section -->
            <h2>💡 Usage</h2>
            <p>
                Once installed, simply run the command in your terminal:
            </p>
            <pre><code>python nymex.py</code></pre>
            <p><strong>Email OSINT Example:</strong></p>
            <pre><code>Enter email to check: johndoe@gmail.com
🔎 Checking across platforms...
✅ Found associated account on Instagram
✅ Found associated account on Twitter
❌ No account found on Facebook</code></pre>
            <p><strong>TryHackMe Profile Example:</strong></p>
            <pre><code>Enter username to search: JohnDoe
🔎 Opening profile for 'JohnDoe'...
✅ Done!</code></pre>
            <!-- Uninstall Section -->
            <h2>🗑️ Uninstall</h2>
            <p>
                To remove the tool from your system:
            </p>
            <pre><code>sudo rm -r nymex</code></pre>
        </article>
        <!-- Footer -->
        <footer>
            <hr>
        </footer>
    </div>
</html>
