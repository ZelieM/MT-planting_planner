console.log('hello');

// Set the min date of SeedingStart to Today
// var today = new Date();
// var todayFormated = today.getFullYear() + '-' + today.getMonth() + 1 + '-' + today.getDate();
// document.getElementById("SeedingStart").min = todayFormated;

// Set the min date of SeedingEnd to the value of SeedingStart
document.getElementById("SeedingStart").addEventListener("change", function (event) {
    var newMinValue = event.srcElement.value;
    console.log(newMinValue);
    document.getElementById('SeedingEnd').min = newMinValue;
});

// Set the min date of HarvestStart to the value of SeedingEnd
document.getElementById("SeedingEnd").addEventListener("change", function (event) {
    var newMinValue = event.srcElement.value;
    document.getElementById('HarvestStart').min = newMinValue;
});

// Set the min date of HarvestEnd to the value of HarvestStart
document.getElementById("HarvestStart").addEventListener("change", function (event) {
    var newMinValue = event.srcElement.value;
    document.getElementById('HarvestEnd').min = newMinValue;
});