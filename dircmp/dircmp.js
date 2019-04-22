const fs = require('fs');

function main() {
    let cmdArgs = process.argv;

    if (cmdArgs.length < 4) {
        console.error('[ERROR] Missing Arguments.');
        console.error(
            'Usage: node dircmp.js ' +
            '"<path/to/first/dir/>" "<path/to/second/dir/>"')
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

    const uniquePathsDir1 = dircmp(dir1, dir2);
    console.log('')
    console.log(`"${dir2}" does not contain,`);
    for (let i = 0; i < uniquePathsDir1.length; i++) {
        const isFileOrDir = 
            uniquePathsDir1[i][uniquePathsDir1[i].length - 1] === '/' ?
            '[DIR]' : '[FIL]';
        console.log(`${i+1}:\t${isFileOrDir}\t${uniquePathsDir1[i]}`)
    }

    const uniquePathsDir2 = dircmp(dir2, dir1);
    console.log('')
    console.log(`"${dir1}" does not contain,`);
    for (let i = 0; i < uniquePathsDir2.length; i++) {
        const isFileOrDir = 
            uniquePathsDir2[i][uniquePathsDir2[i].length - 1] === '/' ?
            '[DIR]' : '[FIL]';
        console.log(`${i+1}:\t${isFileOrDir}\t${uniquePathsDir2[i]}`)
    }
}

function dircmp(dir1, dir2, uniquePaths = []) {
    if (dir1[dir1.length - 1] !== '/') {
        dir1 = dir1 + '/'
    }
    if (dir2[dir2.length - 1] !== '/') {
        dir2 = dir2 + '/'
    }

    const dir1Children = fs.readdirSync(dir1);
    const dir2Children = fs.readdirSync(dir2);

    for (let dir1Child of dir1Children) {
        let isMatchFound = false;
        for (let dir2Child of dir2Children) {
            if (dir1Child === dir2Child) {
                
                const dir1ChildStat = fs.statSync(dir1 + dir1Child);
                const dir2ChildStat = fs.statSync(dir2 + dir2Child);
                
                if (dir1ChildStat.isDirectory()
                        && dir2ChildStat.isDirectory()) {
                    
                    isMatchFound = true;
                    uniquePaths = 
                        dircmp(dir1 + dir1Child, dir2 + dir2Child, uniquePaths);

                } else if (dir1ChildStat.isFile() && dir2ChildStat.isFile()) {
                    isMatchFound = true;
                }
                
            } else {
                // do something here if necessary
            }
        }
        if (!isMatchFound) {
            const pathToAppend = 
                fs.statSync(dir1 + dir1Child).isDirectory() ?
                dir1 + dir1Child + '/' : dir1 + dir1Child;
            uniquePaths.push(pathToAppend);
        }
    }

    return uniquePaths
}

if (require.main === module) {
    main();
}

module.exports = dircmp;

/* 
- get paths of two dirs
- check if both are dirs indeed else throw err
- traverse @param(path1) @param(path2):
    - get list of children from path1
    - get list of children from path2
    - for loop over each path1 child
        - for loop over each path2 child
            - compare if current file/dir is in path 2 children
            - if yes:
                - check if both are dir
                - if yes:
                    - traverse with these two paths as params
                - else:
                    - do something appropriate ...
            - else:
                add to the unique to path1 list

- call traverse for both combs of input dir paths
  first with (path1, path2) then (path2, path1)
*/
