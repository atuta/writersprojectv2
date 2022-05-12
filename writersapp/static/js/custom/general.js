function clearData(){
        window.clipboardData.setData('text','')
    }

    function cldata(){
        if(clipboardData){
            clipboardData.clearData();
        }
    }
    setInterval("cldata();", 1000);