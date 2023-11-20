function App(props){
    let [content,setContent] = React.useState('')
    let [status, setStatus] = React.useState('')
    let [fullscreen, setFullscreen] = React.useState(false)
    let [font,setFont] = React.useState('monospace')
    let [fontsize,setFontsize] = React.useState('12px')
    let [background,setBackground] = React.useState('color-bg-white')
    let [folder,setFolder] = React.useState(true)
    let [sTF, setSTF] = React.useState(false)
    
    var Id = document.getElementById('fileId').value
    //console.log(Id)

    let fetchContent = async ()=>{
        let request = await axios.get(`/filecontent/${Id}`)
        setContent(request.data.content)
        setFolder(request.data.folder)
    }

    fetchContent()

    let saveFile = async ()=>{
        setStatus('saving...')
        let csrf = $('#csrf').val()
        let saveUrl = $('#saveUrl').val()
        let editor = ace.edit('editor')
        let newContent = editor.getValue()
        let data = {'data':newContent}
        let header = {'X-CSRFToken':csrf,/*'Content-Type': 'application/json'*/}
        let request = await axios.post(saveUrl,data, {headers:header})
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
   // editor_read.getSession().setMode('ace/mode/python')
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
  fullscreen ? $('#editor').removeClass('shiftMargin'): $('#editor').addClass('shiftMargin')
},[fullscreen,setFullscreen])

React.useEffect(()=>{
    let timer = setTimeout(()=>setStatus(''),5000)
    return ()=> clearTimeout(timer)
},[status])

    return (
        <div>
        {status}
        <div class={fullscreen ? "row fixed-bottom justify-content-evenly":"row justify-content-evenly"} style={{backgroundColor:'#d1d1d1',left:'0',zIndex:'110000',color:'black'}}>
            <div class="col center ">
                <button class="btn color sz-14" onClick={()=>folder ? saveFile(): setSTF(true)}><i class='fas fa-save'></i> <span class= 'display-sm-none'>save</span></button>
            </div>
            <div class="col center">
                <button class="btn color sz-14" onClick={()=>importFile()}>
                <i class='fas fa-upload'></i>
                <span class='display-sm-none'>
                import</span></button>
            </div>
            <div class="col center">
                <button class="btn color sz-14" onClick={()=>setFullscreen(fullscreen ? false:true)}><i class='fas fa-expand'></i><span class='display-sm-none'>fullscreen
                </span>
                </button>
            </div>
            <div class="col center">
                <button onClick={()=>$('#settings').fadeIn()}  class="btn color sz-14">
                <i class='fas fa-cog'></i>
                <span class='display-sm-none'>
                settings</span></button>
            </div>
        </div>
<div id="editor" classNa={fullscreen ? background :`shiftMargin ${background}`} style={{fontFamily:font,fontSize:fontsize,overFlow:'auto',zIndex:'100000',position:fullscreen ? 'fixed':'absolute',height:'100%',width:'100%',top: fullscreen ?'0':'inherit',left:fullscreen ?'0':'inherit'}}></div>
        <Settings setFont={setFont} setFontSize={setFontsize} setBack={setBackground} />
        {sTF ? <SavetoFolder content={content} setSTF={setSTF} /> : null }
        </div>
        )
}

function SavetoFolder(props ){
  let [folders,setFolders] = React.useState([])
  let fileName = React.useRef()
  let folderId = React.useRef()
  
  let fetchFolder = async ()=>{
    let response = await axios.get(`/getfolders`)
    setFolders(response.data.folders)
  }
  
  let createFile = async ()=>{
    let csrf = $('#csrf').val()
    let Id = $('#fileId').val()
        let saveUrl = '/savefromeditor'
        let editor = ace.edit('editor')
        let newContent = editor.getValue()
        console.log(newContent )
        let data = {'data':newContent,'name':fileName.current.value,'folder':folderId.current.value,'file':Id}
        let header = {'X-CSRFToken':csrf,/*'Content-Type': 'application/json'*/}
        let request = await axios.post(saveUrl,data, {headers:header})
        $('#filename').text(fileName.current.value)
        props.setSTF(false)
     
  }
  
  React.useEffect(()=>{
    fetchFolder()
  },[])
  
  return(
    <div class="modal sz-18" id="settings" style={{zIndex:'1000000',width:'100%',backgroundColor:'rgba(300,300,300,0.9)',display:'block'}}>
        <div class="modal-dialog modal-dialog-centered ">
            <div class="modal-content no-border">
            <div class='modal-content bg-light p-3'>

            <div class='sz-24 color-p my-2'> Save as </div>
            <div class='my-2'><input class='form-control p-2' ref={fileName} name='filename' /></div>
            
           <div class='sz-24 color-p my-2'> Save to</div>
           <select ref={folderId} name='folderId' class='form-control'>
           {
             folders.map((x)=>{return(
               <option value={x.id}>{x.name}</option>
             )})
           }
           
           </select>
            
            <div class='my-2 center'><button class='btn btn-block color-bg-p' onClick={()=>createFile()}>Save file </button></div>
            
            <div class='my-2 center'><button class='btn btn-block ' style={{backgroundColor:'red'}} onClick={()=>props.setSTF(false)}>close </button></div>
            </div>
            </div>
            </div>
            </div>
    )
}

function Settings(props){
  let syntax = React.useRef()
  let font = React.useRef()
  let fontSz = React.useRef() 
  let theme = React.useRef()
 
 let setSyntax = ()=>{
   let mode = syntax.current.value
   let editor = ace.edit('editor');
   editor.session.setMode(`ace/mode/${mode}`)
 } 
 
 let setFont = () =>{
   let fontS= font.current.value
  // let editor = $('#editor').css('font-faily',fontS)
  props.setFont(fontS)
 }
 
 let setFontSize = () =>{
   let fontSize = fontSz.current.value
  // let editor = $('#editor').css('font-faily',fontSize)
  props.setFontSize(fontSize)
 }
 
 let setTheme = () =>{
   let themeS = theme.current.value;
   let editor = ace.edit('editor')
   props.setBack(themeS=='monokai' ? 'color-bg-black':'color-bg-white')
   editor.setTheme(`ace/theme/${themeS}`)
 }
 
  return(
     <div class="modal sz-18" id="settings" style={{zIndex:'1000000',width:'100%',backgroundColor:'rgba(300,300,300,0.9)'}}>
        <div class="modal-dialog modal-dialog-centered ">
            <div class="modal-content no-border">
            <div class='modal-content bg-light p-3'>
            <div class='row my-2'>
            <div class='col sz-24  color-p'>
            settings
            </div>
            </div>
            
            <div class='row my-2'>
            <div class='col sz-20'>
            Theme
            </div>
            </div>
            
            <select class='form-control' ref={theme} onChange={()=>setTheme()}>
            <option value='null'>default </option>
            <option value='monokai' >monokai</option>
            </select>
            
            <div class='row my-2'>
            <div class='col sz-20'>
            syntax
            </div>
            </div>
            
           <select class='form-control' ref={syntax} onChange={()=>setSyntax()} >
            <option value='python'>python </option>
            <option value='javascript'>JavaScript </option>
            <option value='html' >html </option>
           </select>
            
             <div class='row my-2'>
            <div class='col sz-20'>
            Font
            </div>
            </div>
            
            <select class='form-control' ref={font} onChange={()=>setFont()}>
            <option value='monospace'>monospace </option>
            <option value='roboto' >roboto</option>
            <option value='arial'>arial</option>
            </select>
            
            < div class='row my-2'>
            <div class='col sz-20'>
            Font size
            </div>
            </div>
            
              
            <input class='form control' ref={fontSz} type='progress' onChange={()=>setFontSize()} />
            
            
            <div class='row my-2'>
            <div class='col center'>
            <button class='btn btn-block color-white center' style={{backgroundColor:'red'}} onClick={()=>$('#settings').fadeOut()}> close window 
            </button>
            </div>
            </div>
            
            </div>
            </div>
            </div>
            </div>
            
    )
}