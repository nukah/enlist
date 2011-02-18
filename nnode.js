var express = require('express'),
    app = express.createServer(),
    mongoose = require('mongoose'),
    Schema = mongoose.Schema;

mongoose.connect('mongodb://192.168.1.4/notik');

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
app.use(express.staticProvider(__dirname));

mongoose.model('notebook',noteSchema, 'notebooks');

var m = mongoose.model('notebook');
app.get('/', function(req, res) {
	m.find({}, function(err, result) {
		if(err) console.log(err);
		result.sort('doc.added', -1);
		var roster = [];
		result.forEach(function(item) {
			roster.push(item.doc);
		});
		res.render('t', { locals : { list : roster }, layout : false });
	});
});

app.listen(3000);
