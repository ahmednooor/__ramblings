const fs = require('fs');
const dircmp = require('./dircmp');

let cmdArgs = process.argv;
if (cmdArgs.length < 4) {
    console.error('[ERROR] Missing Arguments.');
    console.error(
        'Usage: node main.js <path/to/first/dir> <path/to/second/dir>')
    process.exit()
}

let dir1 = 
    cmdArgs[2][cmdArgs[2].length - 1] !== '/' ?
    cmdArgs[2] + '/' : cmdArgs[2];
let dir2 = 
    cmdArgs[3][cmdArgs[3].length - 1] !== '/' ?
    cmdArgs[3] + '/' : cmdArgs[3];

if (!fs.existsSync(dir1) || !fs.statSync(dir1).isDirectory()) {
    console.error(`[ERROR] "${dir1}" is not a Directory.`);
    process.exit()
}
if (!fs.existsSync(dir2) || !fs.statSync(dir2).isDirectory()) {
    console.error(`[ERROR] "${dir2}" is not a Directory.`);
    process.exit()
}

let uniquePathsDir1 = [];
dircmp(dir1, dir2, uniquePathsDir1);
console.log('')
console.log(`"${dir2}" does not contain,`);
for (let i = 0; i < uniquePathsDir1.length; i++) {
    const isFileOrDir = 
        uniquePathsDir1[i][uniquePathsDir1[i].length - 1] === '/' ?
        '[DIR]' : '[FIL]';
    console.log(`${i+1}: ${isFileOrDir} ${uniquePathsDir1[i]}`)
}

let uniquePathsDir2 = [];
dircmp(dir2, dir1, uniquePathsDir2);
console.log('')
console.log(`"${dir1}" does not contain,`);
for (let i = 0; i < uniquePathsDir2.length; i++) {
    const isFileOrDir = 
        uniquePathsDir2[i][uniquePathsDir2[i].length - 1] === '/' ?
        '[DIR]' : '[FIL]';
    console.log(`${i+1}: ${isFileOrDir} ${uniquePathsDir2[i]}`)
}
