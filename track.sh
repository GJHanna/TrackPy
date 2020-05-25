track(){
   dir="$(pwd)"
   python /YOUR/PATH/TO/TrackPy/trackpy.py $dir $@
   cd
   cd $dir
}