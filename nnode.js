var express = require('express'),
    app = express.createServer(),
    mongoose = require('mongoose'),
    Schema = mongoose.Schema;

mongoose.connect('mongodb://four.eye.rs:27017/notik');

var noteSchema = new Schema({
	added : Date,
	name : String,
	weight : String,
	modified : Date,
	complectations : Array,
});


app.use(express.bodyDecoder());
app.set('views', __dirname);
app.set('view engine', 'jade');
app.set('view options', { layout : false});
app.use(express.staticProvider(__dirname));

mongoose.model('notebook',noteSchema, 'notebooks');

var m = mongoose.model('notebook');
app.get('/', function(req, res) {
	m.find({}, function(err, result) {
		if(err) {
			res.render('t', { locals : { error : err } });
		}
		result.sort('doc.added', -1);
		var roster = [];
		result.forEach(function(item) {
			roster.push(item.doc);
		});
		res.render('t', { locals : { list : roster, count : result.length, error : err} });
	});
});

app.listen(3000);
