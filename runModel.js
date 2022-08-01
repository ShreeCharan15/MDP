const {spawn} = require('child_process');

const runModel=(paths)=>{
    const python = spawn('conda', ['run','-n', 'tf', 'python', 'nst.py','rads.jpeg','wierd.jpg']);
    // collect data from script
    python.stdout.on('data', function (data) {
     console.log('Pipe data from python script ...');
     dataToSend = data.toString();
    });
    python.stderr.on('data',(data)=>{
        console.log(data.toString());
    })

    python.on('error', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        });

    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    });
}
module.exports={runModel}