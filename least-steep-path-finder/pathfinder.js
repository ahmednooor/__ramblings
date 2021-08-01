const gridSizeInput = document.querySelector('#gridSizeInput');
const gridGenBtn = document.querySelector('#gridGenBtn');
const gridCtr = document.querySelector('#gridCtr');

let gridSize = 0;
let startPoint = null;
let destPoint = null;
let curPoint = null;
let grid = [];
let prevSteps = []
let takenSteps = []
let iterations = 1
let numOfSteps = 1

let isStartSelected = false;
let isDestSelected = false;

gridGenBtn.addEventListener('click', (ev) => {
    gridSize = parseInt(gridSizeInput.value, 10);
    gridSize = gridSize < 4 ? 4 : gridSize;
    gridCtr.innerHTML = '';
    grid = [];
    for (let i = 0; i < gridSize; i++) {
        grid.push([]);
        for (let j = 0; j < gridSize; j++) {
            const randNum = getRandomInt(100);
            grid[i].push(randNum);
            const gridBox = `
                <div 
                    style="width: 30px; height: 30px; display: inline-block; padding: 2px; background: #efefef; color: black; border: 1px solid black; font-size: 14px; text-align: center; user-select: none;"
                    id="${'gridBox_' + i.toString() + '_' + j.toString()}"
                    data-row="${i}"
                    data-col="${j}"
                    data-val="${randNum}"
                ><strong style="float: right; font-size: 8px;"></strong>
                <span style="display: inline; vertical-align: bottom; float: left;">${randNum}</span></div>
            `;
            gridCtr.innerHTML += gridBox;
        }
        gridCtr.innerHTML += '<br />';
    }
    const gridBoxes = gridCtr.querySelectorAll('div');
    gridBoxes.forEach(elem => { 
        elem.addEventListener('click', (e) => {
            e.stopPropagation();
            if (!isStartSelected) {
                startPoint = [
                    parseInt(elem.getAttribute('data-row'), 10),
                    parseInt(elem.getAttribute('data-col'), 10),
                    parseInt(elem.getAttribute('data-val'), 10),
                ];
                elem.style.background = 'green';
                elem.style.color = 'white';
                isStartSelected = true;
                document.querySelector('#instructions')
                    .innerHTML = `
                        <em><b>Instructions: </b></em><br />Click a box again to pick as Destination Point
                    `;
            } else if (!isDestSelected) {
                destPoint = [
                    parseInt(elem.getAttribute('data-row'), 10),
                    parseInt(elem.getAttribute('data-col'), 10),
                    parseInt(elem.getAttribute('data-val'), 10),
                ];
                elem.style.background = 'red';
                elem.style.color = 'white';
                isDestSelected = true;
                document.querySelector('#instructions')
                    .innerHTML = `
                        <em><b>Instructions: </b></em><br />Click Start Button
                    `;
                document.querySelector('#results #startBtn').style.display = '';
                document.querySelector('#results #startBtn').addEventListener('click', (evt) => {
                    startProcessing();
                    evt.target.setAttribute('disabled', '');
                });
            }
        }, false);
    });
    document.querySelector('#instructions')
        .innerHTML = `
            <em><b>Instructions: </b></em><br />Click a box to pick as Starting Point
        `;
    gridGenBtn.setAttribute('disabled', '');
});


function startProcessing() {
    
    curPoint = startPoint;
    prevSteps = [startPoint]
    takenSteps = [startPoint]
    
    let reRun = setInterval(() => {
        makePath();
    }, 20);

    function makePath() {

        if (curPoint[0] === destPoint[0] 
            && curPoint[1] === destPoint[1] 
            && curPoint[2] === destPoint[2]) {
                clearInterval(reRun);
                document.querySelector('#results').innerHTML = `
                    <br />
                    <a href="index.html">Reload</a> <br /> <br />
                    Taken Steps: ${JSON.stringify(takenSteps)} <br />
                    Number of Steps: ${takenSteps.length} <br />
                    Iterations took to get valid path: ${iterations} <br />
                `;
                document.querySelector('#instructions')
                    .innerHTML = `
                        <em><b>Instructions: </b></em><br />Process Completed! 'Reload' to Start Again
                    `;
                return;
        }

        let row = curPoint[0];
        let column = curPoint[1];

        let directions = {
            'up': row - 1 < gridSize && row - 1 >= 0 ? [row - 1, column] : null,
            'down': row + 1 < gridSize && row + 1 >= 0 ? [row + 1, column] : null,
            'left': column - 1 < gridSize && column - 1 >= 0 ? [row, column - 1] : null,
            'right': column + 1 < gridSize && column + 1 >= 0 ? [row, column + 1] : null,
        };
        for (let direction in directions ) {
            if (directions[direction] !== null) {
                directions[direction] = [
                    directions[direction][0], 
                    directions[direction][1], 
                    grid[directions[direction][0]][directions[direction][1]],
                ];
                
                for (let i = 0; i < prevSteps.length; i++) {
                    if (isEqual(directions[direction], prevSteps[i])) {
                        directions[direction] = null;
                    }
                }
            }
        }

        if (directions['up'] === null
                && directions['down'] === null
                && directions['left'] === null
                && directions['right'] === null
                && prevSteps.length > 2) {
            curPoint = startPoint;
            prevSteps = prevSteps.slice(
                iterations < prevSteps.length ? -iterations : -1 * getRandomInt(prevSteps.length),
                prevSteps.length
            );
            takenSteps = [];
            numOfSteps = 0;
            iterations += 1;

            updateGrid();
        }

        let nextStep = null;
        let prefSteps = [];

        if (curPoint[2] < destPoint[2]) {
            for (let direction in directions) {
                if (directions[direction] !== null && directions[direction][2] >= curPoint[2]) {
                    prefSteps.push(directions[direction]);
                }
            }
            if (prefSteps.length > 1) {
                for (let direction in prefSteps) {
                    for (let direction_ in prefSteps) {
                        direction = parseInt(direction, 10);
                        direction_ = parseInt(direction_, 10);
                        if (prefSteps[direction_][2] < prefSteps[direction][2]) {
                            nextStep = prefSteps[direction_];
                        }
                    }
                }
            } else if (prefSteps.length === 1) {
                nextStep = prefSteps[0];
            } else {
                prefSteps = []
                for (let direction in directions) {
                    if (directions[direction] !== null && directions[direction][2] <= curPoint[2]) {
                        prefSteps.push(directions[direction]);
                    }
                }
                if (prefSteps.length > 1) {
                    for (let direction in prefSteps) {
                        for (let direction_ in prefSteps) {
                            direction = parseInt(direction, 10);
                            direction_ = parseInt(direction_, 10);
                            if (prefSteps[direction_][2] > prefSteps[direction][2]) {
                                nextStep = prefSteps[direction_];
                            }
                        }
                    }
                } else if (prefSteps.length === 1) {
                    nextStep = prefSteps[0];
                }
            }

            if (nextStep !== null) {
                curPoint = nextStep;
            } else {
                for (let direction in directions) {
                    if (directions[direction] !== null) {
                        curPoint = directions[direction];
                        break;
                    }
                }
            }
        } else if (curPoint[2] >= destPoint[2]) {
            for (let direction in directions) {
                if (directions[direction] !== null && directions[direction][2] <= curPoint[2]) {
                    prefSteps.push(directions[direction]);
                }
            }
            if (prefSteps.length > 1) {
                for (let direction in prefSteps) {
                    for (let direction_ in prefSteps) {
                        direction = parseInt(direction, 10);
                        direction_ = parseInt(direction_, 10);
                        if (prefSteps[direction_][2] > prefSteps[direction][2]) {
                            nextStep = prefSteps[direction_];
                        }
                    }
                }
            } else if (prefSteps.length === 1) {
                nextStep = prefSteps[0];
            } else {
                prefSteps = [];
                for (let direction in directions) {
                    if (directions[direction] !== null && directions[direction][2] >= curPoint[2]) {
                        prefSteps.push(directions[direction]);
                    }
                }
                if (prefSteps.length > 1) {
                    for (let direction in prefSteps) {
                        for (let direction_ in prefSteps) {
                            direction = parseInt(direction, 10);
                            direction_ = parseInt(direction_, 10);
                            if (prefSteps[direction_][2] < prefSteps[direction][2]) {
                                nextStep = prefSteps[direction_];
                            }
                        }
                    }
                } else if (prefSteps.length === 1) {
                    nextStep = prefSteps[0];
                }
            }

            if (nextStep !== null) {
                curPoint = nextStep;
            } else {
                for (let direction in directions) {
                    if (directions[direction] !== null) {
                        curPoint = directions[direction];
                        break;
                    }
                }
            }
        }

        takenSteps.push(curPoint);
        let curPointInPrevSteps = true;
        for (let step in prevSteps) {
            step = parseInt(step, 10);
            if (isEqual(curPoint, prevSteps[step])) {
                curPointInPrevSteps = true;
            } else {
                curPointInPrevSteps = false;
            }
        }
        if (!curPointInPrevSteps)
            prevSteps.push(curPoint);
        
        updateGrid();

    }
}

function updateGrid() {
    for (let i in grid) {
        for (let j in grid[i]) {
            i = parseInt(i, 10);
            j = parseInt(j, 10);
            const tempPoint = [i, j, grid[i][j]];
            if (!isEqual(tempPoint, startPoint) && !isEqual(tempPoint, destPoint)) {
                let elem = document.querySelector(`#gridBox_${i}_${j}`);
                elem.style.background = '#efefef';
                elem.style.color = 'black';
                elem.querySelector('strong').innerHTML = ``;
            }
        }
    }
    for (let i in prevSteps) {
        if (!isEqual(prevSteps[i], startPoint) && !isEqual(prevSteps[i], destPoint)) {
            let elem = document.querySelector(`#gridBox_${prevSteps[i][0]}_${prevSteps[i][1]}`);
            elem.style.background = '#aaaaaa';
            elem.style.color = '#efefef';
            elem.querySelector('strong').innerHTML = ``;
        }
    }
    for (let i in takenSteps) {
        let elem = document.querySelector(`#gridBox_${takenSteps[i][0]}_${takenSteps[i][1]}`);
        if (!isEqual(takenSteps[i], startPoint) && !isEqual(takenSteps[i], destPoint)) {
            elem.style.background = 'blue';
            elem.style.color = 'white';
        }
        elem.querySelector('strong').innerHTML = `${i}`;
    }
}


// taken from MDN
function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}


// taken from https://gomakethings.com/check-if-two-arrays-or-objects-are-equal-with-javascript/
var isEqual = function (value, other) {

	// Get the value type
	var type = Object.prototype.toString.call(value);

	// If the two objects are not the same type, return false
	if (type !== Object.prototype.toString.call(other)) return false;

	// If items are not an object or array, return false
	if (['[object Array]', '[object Object]'].indexOf(type) < 0) return false;

	// Compare the length of the length of the two items
	var valueLen = type === '[object Array]' ? value.length : Object.keys(value).length;
	var otherLen = type === '[object Array]' ? other.length : Object.keys(other).length;
	if (valueLen !== otherLen) return false;

	// Compare two items
	var compare = function (item1, item2) {

		// Get the object type
		var itemType = Object.prototype.toString.call(item1);

		// If an object or array, compare recursively
		if (['[object Array]', '[object Object]'].indexOf(itemType) >= 0) {
			if (!isEqual(item1, item2)) return false;
		}

		// Otherwise, do a simple comparison
		else {

			// If the two items are not the same type, return false
			if (itemType !== Object.prototype.toString.call(item2)) return false;

			// Else if it's a function, convert to a string and compare
			// Otherwise, just compare
			if (itemType === '[object Function]') {
				if (item1.toString() !== item2.toString()) return false;
			} else {
				if (item1 !== item2) return false;
			}

		}
	};

	// Compare properties
	if (type === '[object Array]') {
		for (var i = 0; i < valueLen; i++) {
			if (compare(value[i], other[i]) === false) return false;
		}
	} else {
		for (var key in value) {
			if (value.hasOwnProperty(key)) {
				if (compare(value[key], other[key]) === false) return false;
			}
		}
	}

	// If nothing failed, return true
	return true;

};