var fs = require('fs');

var print = s => ("      " + s).substr(-6);

var r = [];

var files = fs.readdirSync('./json'); 
files.forEach(file=>{
  // var body = JSON.parse(fs.readFileSync('./feeds/'+file)); 
  // if ( (ch = body.channel) && ch.id ) {
    var id = file.split('.')[0];
    r[id/1e5|0] = (r[id/1e5|0]||0) + 1
  // }
});

r.forEach((a,b)=>{
  console.log(print(b + "*****"),a);
})
console.log(files.length);
