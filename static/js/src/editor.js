function App(props){
    let [content,setContent] = React.useState('how are you')
    let [status, setStatus] = React.useState('')
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
    },[fetchContent,content])

React.useEffect(()=>{
    let timer = setTimeout(()=>setStatus(''),5000)
    return ()=> clearTimeout(timer)
},[status])
    return (
        <div>
        {status}
        <div class="row" style={{backgroundColor:'#d1d1d1'}}>
            <div class="col">
                <button class="btn" onClick={()=>saveFile()}>save</button>
            </div>
            <div class="col">
                <button class="btn">import</button>
            </div>
        </div>
        <div id="editor" style={{height:"100%",width:'80%'}}>
        
        
        </div>
        </div>
        )
}