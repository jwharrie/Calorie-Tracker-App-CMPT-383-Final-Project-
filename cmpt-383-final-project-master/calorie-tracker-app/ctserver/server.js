const express = require('express')
const fs = require('fs')

var app = express()

const USER_FILEPATH = __dirname + '/data/users.json'
const FOOD_FILEPATH = __dirname + '/data/foods.json'

// UNUSED
app.get('/list_users', (req, res) => {
	fs.readFile(USER_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		console.log(data);
		res.end();
	});
})

// Tests connection at start-up
app.get('/test', (req, res) => {
    res.send("secret message");
})

// Checks if user exists in users.json
app.get('/check_user', (req, res) => {
	fs.readFile(USER_FILEPATH, 'utf8', (err, data) => {
		users = JSON.parse(data);
		u = req.query.u;
		if (u in users) {
			res.send("1");
		}
		else {
			res.send("0")
		}
	});
})

// Check if food exists in foods.json
app.get('/check_food', (req, res) => {
	fs.readFile(FOOD_FILEPATH, 'utf8', (err, data) => {
		foods = JSON.parse(data);
		f = req.query.f;
		if (f in foods) {
			res.send("1");
		}
		else {
			res.send("0")
		}
	});
})

// Helps with login
app.get('/login', (req, res) => {
	const q = req.query;
	fs.readFile(USER_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		if (!(q.u in data)) {
			res.json(null);
		}
		else {
			user = data[q.u];
			if(q.pw != user['password']) {
				res.json(null);
			}
			else {
				res.json(user);
			}
		}
	});
})

// Get food object with name q
app.get('/get_food', (req, res) => {
	const q = req.query.q;
	fs.readFile(FOOD_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		if (q in data) {
			food = data[q];
			res.json(food);
		}
		else {
			res.json(null);
		}
	});
})

// Send back list of all food objects
app.get('/get_all_foods', (req, res) => {
	fs.readFile(FOOD_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		res.json(data);
	});
})

// Creates and adds user object to users.json
app.post('/add_user', (req, res) => {
	const q = req.query;
	const user = {
		'username': q.username,
		'password': q.pw,
		'first_name': q.first_name,
		'last_name': q.last_name,
		'age': parseInt(q.age),
		'gender': q.gender,
		'height': parseFloat(q.height),
		'activity_level': q.activity_level,
		'goal': q.goal,
		'weight_history': {},
		'cal_history': {},
		'weight_today': 0,
		'cal_today': 0
	};
	fs.readFile(USER_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		data[q.username] = user;
		fs.writeFileSync(USER_FILEPATH, JSON.stringify(data));
		res.end();
	});
})

// Creates and adds food object to foods.json
app.post('/add_food', (req, res) => {
	const q = req.query;
	const food = {
		'name': q.name,
		'calories': parseFloat(q.cal),
		'serving_size': parseFloat(q.serving_size)
	};
	fs.readFile(FOOD_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		data[q.name] = food;
		fs.writeFileSync(FOOD_FILEPATH, JSON.stringify(data));
		res.end();
	});
})

// Modifies user object
app.post('/update/user/:to_update', (req, res) => {
	const q = req.query;
	const p = req.params.to_update
	fs.readFile(USER_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		var user = data[q.username];
		switch (p) {
			case 'weight':
				const w = parseFloat(q.val);
				user.weight_history[q.date] = w;
				user.weight_today = w;
				break;
			case 'cal':
				const c = parseFloat(q.val);
				user.cal_history[q.date] += c;
				user.cal_today += c;
				break;
			case 'age':
				user['age'] = parseInt(q.val);
				break;
			case 'height':
				user['height'] = parseFloat(q.val);
				break;
			default:
				user[p] = q.val;
		}
		data[q.username] = user;
		fs.writeFileSync(USER_FILEPATH, JSON.stringify(data));
		res.json(user);
	});
})

// Modifies food object
app.post('/update/food/:to_update', (req, res) => {
	const q = req.query;
	const p = req.params.to_update;
	fs.readFile(FOOD_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		var food = data[q.name]
		switch (p) {
			case 'calories':
				const cal = parseFloat(q.val);
				food['calories'] = cal;
				break;
			case 'serving_size':
				const size = parseFloat(q.val);
				food['serving_size'] = size;
				break;
		}
		data[q.name] = food;
		fs.writeFileSync(FOOD_FILEPATH, JSON.stringify(data));
		res.end();
	});
})

// Delete food object from foods.json
app.delete('/delete_food', (req, res) => {
	const f = req.query.f;
	fs.readFile(FOOD_FILEPATH, 'utf8', (err, data) => {
		data = JSON.parse(data);
		delete data[f];
		fs.writeFileSync(FOOD_FILEPATH, JSON.stringify(data));
		res.end();
	});
})

// Server listener code
var server = app.listen(8080, () => {
    var port = server.address().port;
    console.log('Node.js server on. Listening at http://localhost:%s', port)
})