import fs from 'fs-extra';
import path from 'path';
import archiver from 'archiver';
import extract from 'extract-zip';
import { fileURLToPath } from 'url';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.resolve(__dirname, '..');
const srcDir = path.join(rootDir, 'src');
const releasesDir = path.join(rootDir, 'releases');
const initFile = path.join(srcDir, '__init__.py');
async function getBlenderPaths(): Promise<string[]> {
    const homeDir = os.homedir();
    const platform = process.platform;

    let blenderBaseDir: string;

    if (platform === 'win32') {
        // Windows: %APPDATA%\Blender Foundation\Blender\
        blenderBaseDir = path.join(homeDir, 'AppData', 'Roaming', 'Blender Foundation', 'Blender');
    } else if (platform === 'darwin') {
        // macOS: ~/Library/Application Support/Blender/
        blenderBaseDir = path.join(homeDir, 'Library', 'Application Support', 'Blender');
    } else {
        console.log('Unsupported platform. Only Windows and macOS are supported.');
        return [];
    }

    // Check if the base directory exists
    if (!fs.existsSync(blenderBaseDir)) {
        console.log(`Blender base directory not found: ${blenderBaseDir}`);
        return [];
    }

    // Read all version folders (e.g., "4.4", "5.0")
    const entries = await fs.readdir(blenderBaseDir, { withFileTypes: true });
    const blenderPaths: string[] = [];

    for (const entry of entries) {
        if (entry.isDirectory()) {
            const versionPath = path.join(blenderBaseDir, entry.name);
            const addonsPath = path.join(versionPath, 'scripts', 'addons');

            // Validate that this is a valid Blender installation
            if (fs.existsSync(addonsPath)) {
                blenderPaths.push(versionPath);
                console.log(`Found Blender ${entry.name}: ${versionPath}`);
            }
        }
    }

    if (blenderPaths.length === 0) {
        console.log('No valid Blender installations found.');
    }

    return blenderPaths;
}

async function getVersion(): Promise<string> {
    if (!fs.existsSync(initFile)) {
        throw new Error(`Could not find ${initFile}`);
    }
    const content = await fs.readFile(initFile, 'utf-8');
    const versionMatch = content.match(/"version":\s*\((\d+),\s*(\d+)(?:,\s*(\d+))?\)/);

    if (!versionMatch) {
        throw new Error('Could not find version in __init__.py');
    }

    const major = versionMatch[1];
    const minor = versionMatch[2];
    const patch = versionMatch[3] || '0';

    return `${major}.${minor}.${patch}`;
}

async function createZip(version: string) {
    await fs.ensureDir(releasesDir);

    const versionedZipName = `searchExtension_v${version}.zip`;
    const latestZipName = `searchExtension_latest.zip`;

    const versionedZipPath = path.join(releasesDir, versionedZipName);
    const latestZipPath = path.join(releasesDir, latestZipName);

    // Create versioned zip
    await zipDirectory(srcDir, versionedZipPath, 'searchExtension');
    console.log(`Created ${versionedZipName}`);

    // Create latest zip (copy)
    await fs.copy(versionedZipPath, latestZipPath);
    console.log(`Created ${latestZipName}`);

    return { versionedZipPath, latestZipPath };
}

function zipDirectory(sourceDir: string, outPath: string, zipRootName: string): Promise<void> {
    return new Promise((resolve, reject) => {
        const output = fs.createWriteStream(outPath);
        const archive = archiver('zip', {
            zlib: { level: 9 }
        });

        output.on('close', () => resolve());
        archive.on('error', (err) => reject(err));

        archive.pipe(output);
        archive.directory(sourceDir, zipRootName);
        archive.finalize();
    });
}


async function deployToBlender(
    blenderPaths: string[],
    version: string,
    latestZipPath: string
): Promise<void> {
    if (blenderPaths.length === 0) {
        console.log('No Blender installations found. Skipping deployment.');
        return;
    }

    console.log('\nStarting deployment to Blender installations...');

    for (const blenderPath of blenderPaths) {
        console.log(`\nDeploying to: ${blenderPath}`);

        const addonsPath = path.join(blenderPath, 'scripts', 'addons');
        const addonPath = path.join(addonsPath, 'searchExtension');

        try {
            // Remove existing addon if it exists
            if (fs.existsSync(addonPath)) {
                await fs.remove(addonPath);
                console.log(`  Removed existing: searchExtension`);
            }

            // Extract latest zip
            await extract(latestZipPath, { dir: addonsPath });

            console.log(`  ✓ Deployed: searchExtension v${version}`);
        } catch (error) {
            console.error(`  ✗ Failed to deploy:`, error);
        }
    }

    console.log('\nDeployment complete!');
}

async function main() {
    try {
        console.log('Starting build...');
        const version = await getVersion();
        console.log(`Detected version: ${version}`);

        const { versionedZipPath, latestZipPath } = await createZip(version);
        console.log('Build complete!');

        // Auto-detect Blender installations and deploy
        console.log('\nDetecting Blender installations...');
        const blenderPaths = await getBlenderPaths();

        if (blenderPaths.length > 0) {
            await deployToBlender(blenderPaths, version, latestZipPath);
        }
    } catch (error) {
        console.error('Build failed:', error);
        process.exit(1);
    }
}

main();

