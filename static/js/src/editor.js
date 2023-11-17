function App(props){
    let [content,setContent] = React.useState('')
    let [status, setStatus] = React.useState('')
    let [fullscreen, setFullscreen] = React.useState(false)
    var Id = document.getElementById('fileId').value
    //console.log(Id)

    let fetchContent = async ()=>{
        let request = await axios.get(`filecontent/${Id}`)
        setContent(request.data.content)
    }

    fetchContent()

    let saveFile = async ()=>{
        let csrf = $('#csrf').val()
        let editor = ace.edit('editor')
        let newContent = editor.getValue()
        let data = {'data':newContent}
        let header = {'X-CSRFToken':csrf,/*'Content-Type': 'application/json'*/}
        let request = await axios.post(`savefile/${Id}`,data, {headers:header})
        setStatus(request.data.content)
        setContent(newContent)

    }

    let fullscreenEditor= () => {
            <div id="editor" style={{height:"100%",width:'80%'}}>
        </div>        
    }

    let smallScreenEditor = () => <div id="editor" style={{height:"100%",width:'80%'}}>  </div>
    
    let importFile = ()=>{
        $('#import').fadeIn()
    }

    React.useEffect(()=>{
    //ace.config.set('modePath', "{%static 'js'%}")
    let editor_read = ace.edit('editor')
    editor_read.setValue(content)
    //editor_read.setTheme('ace/theme/monokai');
    //editor_read.setReadOnly(false)
    editor_read.getSession().setMode('ace/mode/python')
    editor_read.getSession().on('change',()=>{
    var currentValue = editor_read.getValue();

  // Compare with the initial value to check if it has changed
  if (currentValue !== content) {
    //setStatus('not saved')
    // Perform any actions you need when the value changes
  }
  })
    },[fetchContent,content,fullscreen])

React.useEffect(()=>{
    let timer = setTimeout(()=>setStatus(''),5000)
    return ()=> clearTimeout(timer)
},[status])

    return (
        <div>
        {status}
        <div class={fullscreen ? "row fixed-bottom justify-content-evenly":"row justify-content-evenly"} style={{backgroundColor:'#d1d1d1',left:'0',zIndex:'110000',color:'black'}}>
            <div class="col">
                <button class="btn color-" onClick={()=>saveFile()}>save</button>
            </div>
            <div class="col">
                <button class="btn color-" onClick={()=>importFile()}>import</button>
            </div>
            <div class="col">
                <button class="btn color-" onClick={()=>setFullscreen(fullscreen ? false:true)}>fullscreen</button>
            </div>
        </div>
        <div id="editor" class="color-bg-white" style={{zIndex:'100000',position:'fixed',height:'100%',width:'100%',top: fullscreen ?'0':'inherit',left:fullscreen ?'0':'inherit'}}>  </div>
        </div>
        )
}