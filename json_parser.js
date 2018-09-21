var fs = require('fs');

var print = s => ("      " + s).substr(-6);

var r = [], x = {};

var files = fs.readdirSync('./json'); 
files.forEach(file=>{
  var body = JSON.parse(fs.readFileSync('./json/'+file).replace(': ]',':""]')); 
  if ( body.author) {
    x[body.author] = (x[body.author]||0) + 1;
    // r[+ch.id] = [ch.created_at,ch.updated_at];
  }
});

// r.forEach((a,b)=>{
//   console.log(print(b),a[0],a[1]);
// })

for (var t of Object.keys(x).sort(((a,b)=>x[a]-x[b]))) {
  console.log(t,x[t]);
} 