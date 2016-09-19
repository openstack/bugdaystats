function convData(jsondata) {
  var newEnt = [];
  var criticalEnt = [];
  var highEnt = [];
  var inProgEnt = [];
  var totalOpen = [];

  var records = jsondata['records'];
  for (ent in records) {
    console.debug(records[ent]);
    var xval = records[ent]['date'] * 1000;
    newEnt.push({
      x: xval,
      y: records[ent]['new']
    });
    criticalEnt.push({
      x: xval,
      y: records[ent]['critical']
    });
    highEnt.push({
      x: xval,
      y: records[ent]['high']
    });
    inProgEnt.push({
      x: xval,
      y: records[ent]['inprogress']
    });
    totalOpen.push({
      x: xval,
      y: records[ent]['new']+records[ent]['incomplete']+records[ent]['inprogress']+records[ent]['confirmed']+records[ent]['triaged']
    });
  }
  var bugsData = [
    { key: 'New', values: newEnt, area: false, type: 'line', color: 'pink' },
    { key: 'Critical', values: criticalEnt, area: false, type: 'line', color: 'red'},
    { key: 'High', values: highEnt, area: false, type: 'line', color: 'orange'},
    { key: 'In Progress', values: inProgEnt, area: false, type: 'line', color: 'skyblue'},
    { key: 'Total Open', values: totalOpen, area: false, type: 'line', color: 'lightgreen'}
  ];
  return bugsData;
}
