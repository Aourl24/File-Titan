class App extends React.Component{
constructor(props){
super(props);
this.state={background:'#000000', color:'#ffffff', font:'12px', mode:'javascript', word:'Welcome to Editor'}
}

changeB =(e)=>{
e.preventDefault();
var b=$('#BC').val();
var a=$('#C').val();
var c=$('#D').val();
var d=$('#M').val();
this.setState({mode:d, background:b, color:a, font:c});
var editor=ace.edit('editor');
editor.session.setMode(`ace/mode/${d}`);
}

showS=(e)=>{
$('#setting').toggleClass('show')

}

preview(){
$('.edit').toggleClass('fullscreen');
}

componentDidMount(){
var editor=ace.edit('editor');
var modelist=ace.require('ace/ext/modelist')
editor.setTheme('ace/theme/monokai');
var full_path=document.getElementById('filepath').value;
console.log('path is ' + full_path);
var mode=modelist.getModeForPath(full_path);
//editor.session.setMode(`ace/mode/${this.state.mode}`);
editor.session.setMode(mode.mode);
editor.setOptions({
highlightActiveLine: false, // boolean
highlightSelectedWord: true, 
//showLineNumbers:false,
showPrintMargin:false, 
}
)

//$('#ed').submit(function(){var code=editor.getValue();$('#ov').val(code)})

}

componentWillMount(){
var b=$('#cov').val();
this.setState({word:b})
}

render(){

var sty={backgroundColor:this.state.background, color:this.state.color, fontSize:this.state.font,height:'80%',  top:0, bottom:0, left:0, right:0, brder:'1px solid black'}
return(
	<div>
	    <div className='left'>
				<button class='sticker'  draggable type='button' style={{position:'fixed', right:'25px',bottom:'80px'}} onClick={this.preview} > <i class='fas fa-eye'></i> 
				</button>
		</div>
		
		<div id='editor' class='edit' style={sty} >
			{this.state.word}
		</div>
        
        
		<div className=''>
		<button className='sticker' draggable type='button' onClick={this.showS} style={{position:'fixed', right:'25px',bottom:'120px'}} > <i class='fas fa-pen'></i> </button>
		</div>
		<div className='pop setting'>
		<form method='GET' id='setting' className='bpop hide' onSubmit={this.changeB} >
		<p>
		<input id='BC' type='color' vale='{this.state.background}' className='input' onChange={this.ChangeB} /> <div 
		className='desize'> Background Color</div>
		</p>
		<hr/>
		<p>
		<input id='C' className='input' type='color' vale={this.state.color} /> <div className='desize'>Font Color </div>
		</p>
		<hr/>
		<p>
		<input id='D' className='input' vale={this.state.font} type='range' /> <div class='desize'>Change Font </div>
		</p>
		<hr/>
		<p>
		<input id='M' className='input setting' /> <div class='desize'>Change Mode </div>
		</p>
		<hr/>
		<button class='button' type='submit'> Save Setting </button>
		</form>
		</div>
	</div>


)

}
}

/*var editor=ace.edit('editor');
editor.setTheme('ace/theme/monokai');
editor.session.setMode('ace/mode/python')
*/
var part=document.getElementById('edit')
ReactDOM.render(<App />, part)
 //<div><span class='circle'>