var fs = require('fs');

var print = s => ("      " + s).substr(-6);

var r = [], x = {};

var files = fs.readdirSync('./feeds'); 
files.forEach(file=>{
  var body = JSON.parse(fs.readFileSync('./feeds/'+file)); 
  if ( (ch = body.channel) && ch.created_at ) {
    var t = ch.created_at.substr(0,7);
    x[t] = (x[t]||0) + 1;
    r[+ch.id] = [ch.created_at,ch.updated_at];
  }
});

r.forEach((a,b)=>{
  console.log(print(b),a[0],a[1]);
})

for (var t of Object.keys(x).sort()) {
  console.log(t,x[t]);
}