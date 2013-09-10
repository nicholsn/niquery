var volume;
var sliceX;
var sliceY;
var sliceZ;

function display_slices() 
{

  //
  // create the 2D renderers
  // .. for the X orientation
  sliceX = new X.renderer2D();
  sliceX.container = 'sliceX';
  sliceX.orientation = 'X';
  sliceX.init();
  // .. for Y
  var sliceY = new X.renderer2D();
  sliceY.container = 'sliceY';
  sliceY.orientation = 'Y';
  sliceY.init();
  // .. and for Z
  var sliceZ = new X.renderer2D();
  sliceZ.container = 'sliceZ';
  sliceZ.orientation = 'Z';
  sliceZ.init();
  

  //
  // THE VOLUME DATA
  //
  // create a X.volume
  volume = new X.volume();
  // .. and attach the single-file dicom in .nii.gz format
  volume.file = 'MNI152_T1_1mm.nii';
  
  // add the volume in the main renderer
  // we choose the sliceX here, since this should work also on
  // non-webGL-friendly devices like Safari on iOS
  sliceX.add(volume);
  
  // start the loading/rendering
  sliceX.render();
  

  //
  // THE GUI
  //
  // the onShowtime method gets executed after all files were fully loaded and
  // just before the first rendering attempt
  sliceX.onShowtime = function() {

    //
    // add the volume to the other 2 renderers
    //
    sliceY.add(volume);
    sliceY.render();
    sliceZ.add(volume);
    sliceZ.render();
    
    // now the real GUI
    var gui = new dat.GUI();
    
    // the following configures the gui for interacting with the X.volume
    var volumegui = gui.addFolder('Volume');
    // .. and the threshold in the min..max range
    var lowerThresholdController = volumegui.add(volume, 'lowerThreshold',
        volume.min, volume.max);
    var upperThresholdController = volumegui.add(volume, 'upperThreshold',
        volume.min, volume.max);
    var lowerWindowController = volumegui.add(volume, 'windowLow', volume.min,
        volume.max);
    var upperWindowController = volumegui.add(volume, 'windowHigh', volume.min,
        volume.max);
    // the indexX,Y,Z are the currently displayed slice indices in the range
    // 0..dimensions-1
    var sliceXController = volumegui.add(volume, 'indexX', 0,
        volume.dimensions[0] - 1);
    var sliceYController = volumegui.add(volume, 'indexY', 0,
        volume.dimensions[1] - 1);
    var sliceZController = volumegui.add(volume, 'indexZ', 0,
        volume.dimensions[2] - 1);
    volumegui.open();
    
  };
  
}