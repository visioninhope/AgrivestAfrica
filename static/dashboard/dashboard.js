const prods = document.querySelectorAll('[id=prod_a]')
if(prods){
  for (let i = 0; i < prods.length; i++) {
    prods[i]
    console.log()
    anime({
      targets: prods[i],
      opacity : [0,1],
      translateX: [-100,0],
      duration: parseInt(200) * parseInt(i+1),
      delay: parseInt(100) * parseInt(i+1)
    });
  }
}

const main_top = document.querySelector('.main_top')
const main_low  = document.querySelector('.main_low')
const prod_box_tag = document.getElementById('prod_box_tag')

if(prod_box_tag){
  prod_box_tag.onclick =()=>{
  main_top.classList.toggle('change')
  main_low.classList.toggle('change')
  prod_box_tag.classList.toggle('change')
  }
}

const left = document.querySelector('.left')
const left_top = document.getElementById('left_top')
const user_con = document.querySelector('.user_con')
const menu_a = document.querySelectorAll('[id=menu_a]')
const menu_ab = document.querySelectorAll('[id=menu_ab]')
const left_tag = document.getElementById('left_tag')
const left_tag_2 = document.getElementById('left_tag_2')
const left_close_tag = document.getElementById('left_close_tag')
const logout = document.getElementById('logout')
const main = document.querySelector('.main')
const main_cover = document.querySelector('.main_cover')

const expand = document.getElementById('expand')
const exp_menu = document.getElementById('exp_menu')

if(expand){
  expand.onclick =()=>{
    exp_menu.classList.toggle('change')
  }
}

left_tag_2.onclick =()=>{
  left.classList.add('mini')
  main_cover.classList.add('change')
}
left_close_tag.onclick =()=>{
  left.classList.remove('mini')
  main_cover.classList.remove('change')
}


if(left_tag){
  left_tag.onclick =()=>{
    console.log('me')
    left.classList.toggle('change')
    left_tag.classList.toggle('change')
    left_top.classList.toggle('change')
    user_con.classList.toggle('change')
    logout.classList.toggle('change')
    main.classList.toggle('change')
    menu_a.forEach(a=>{
      a.classList.toggle('change')
    })
    menu_ab.forEach(a=>{
      a.classList.toggle('change')
    })
    exp_menu.classList.toggle('mini')
  } 
}

const inp = document.querySelectorAll('.pro_set')
const pic_box = document.querySelectorAll('[id=pic_box]')
if (inp) { 
  for (let i = 0; i < inp.length; i++) {
    inp[i].onchange =()=> {
      const [file] = inp[i].files
      pic_box[i].src = URL.createObjectURL(file)
      console.log(pic_box[i].src) 
    }
  }
}



if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}