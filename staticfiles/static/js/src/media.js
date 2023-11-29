function App(props){
	var Id = document.getElementById('fileId').value
	let [content,setContent] = React.useState()
	let [fullscreen, setFullscreen] = React.useState(false)
	let fetchData = async () =>{ 
		let response = await axios.get(`getImage/${Id}`)
		setContent(response.data.image)
	}
	fetchData()

	React.useEffect(()=>{

	},[])

	return(
			<div>
				<div class={fullscreen ? "row fixed-bottom color-bg-p":"row color-bg-p"} style={{backgroundColr:'#d1d1d1',left:'0',zIndex:'110000',color:'white'}}>
            <div class="col">
                <a class="btn color-white" href={content} download>Download image</a>
            </div>
            <div class="col">
                <button class="btn color-white" onClick={()=>setFullscreen(fullscreen ? false:true)}>fullscreen</button>
            </div>
        </div>
        <br />

					{fullscreen ? <img src={content} className="" style={{zIndex:'100000',position:'fixed',height:'100%',width:'100%',top:'0',left:'0',objectFit:'contain',backgroundColor:'white'}}/> : <img src={content} className="img-fluid container" style={{height:'400px',objectFit:'contain'}}/>}
					
			</div>
		)
}