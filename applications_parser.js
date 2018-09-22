var fs = require('fs');

var print = s => ("           " + s).substr(-11);

var cx = {};

var categories = JSON.parse(fs.readFileSync('./categories.json'));
var graphs     = JSON.parse(fs.readFileSync('./chart_type.json'));

for (g of graphs) {
  for (c of categories) {
    if (c.channel_num == g.channel_num) {
      cx[c.type] = cx[c.type] || {};
      cx[c.type][g.plot] = (cx[c.type][g.plot]||0) + 1;
    }
  }
}

var r = {
  "line":'"Line Plot"',
  "spline":'"Spline Plot"',
  "status":'"Status"',
  "map":'"Location Map"',
  "unknown":'"Plugin"',
  "column":'"Column Plot"',
  "video":'"Video"',
  "step":'"Step Plot"',
  "bar":'"Bar Plot"',
}

// Write to files
for (c in cx) {
  var s = "type count\n";
  for (g in r)
    s += r[g] + ' ' + (cx[c][g]||0) + '\n';
  fs.writeFileSync('./applications/'+c+'.txt',s);
}

console.log(categories.length);

cx={}
for (c of categories) {
  cx[c.type] = (cx[c.type] || 0) + 1;
}
console.log(cx);