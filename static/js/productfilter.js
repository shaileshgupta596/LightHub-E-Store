
  function p_type_checkbox(x){
    b = document.getElementsByClassName('p_type_checkbox');
    console.log(b.length);
    for(var i=0 ; i < b.length ;i++){
      if (b[i] != x){
        b[i].checked =false;
      }
      
    }
    x.checked=true;
  }

  function brand_checkbox_work(x){
    b = document.getElementsByClassName('brand_checkbox');
    if (x.checked == true && x.value == 'All'){
        for(var i=0 ; i < b.length ;i++){
        if(b[i]!=x){
          b[i].checked = false;
        }
      }
        
    }

    if (x.checked == true && x.value != 'All'){
        for(var i=0 ; i < b.length ;i++){
        if(b[i].value=="All"){
          b[i].checked = false;
        }
      }
        
    }
    main();
  }
  function product_checkbox_work(x){
    b = document.getElementsByClassName('product_checkbox');
    if (x.checked == true && x.value == 'All'){
        for(var i=0 ; i < b.length ;i++){
        if(b[i]!=x){
          b[i].checked = false;
        }

      }
        
    }

    if (x.checked == true && x.value != 'All'){
        for(var i=0 ; i < b.length ;i++){
        if(b[i].value=="All"){
          b[i].checked = false;
        }
      }
        
    }
    main();
  }
  function p_type_checkbox(){
    
    b = document.getElementsByClassName('p_type_checkbox');
    //console.log(b.length);
    for(var i=0 ; i < b.length ;i++){
      if (b[i].checked == true){
        return b[i].value
      } 
    }
  }
  function brand_checkbox(){

    var brand_list=[]
    b = document.getElementsByClassName('brand_checkbox');
    //console.log(b.length);
    for(var i=0 ; i < b.length ;i++){
      if (b[i].checked == true){
        brand_list.push(b[i].value)
      } 
    }
    return brand_list
  }
  function price_checkbox(){
    
    b = document.getElementsByClassName('price_checkbox');
    //console.log(b.length);
    for(var i=0 ; i < b.length ;i++){
      if (b[i].checked == true){
        return b[i].value
      } 
    }

  }
  function product_checkbox(){
    var brand_list=[]
    b = document.getElementsByClassName('product_checkbox');
    //console.log(b.length);
    for(var i=0 ; i < b.length ;i++){
      if (b[i].checked == true){
        brand_list.push(b[i].value)
      } 
    }
    return brand_list
  }

  function p_warranty_checkbox(){
    
    b = document.getElementsByClassName('p_warranty_checkbox');
    //console.log(b.length);
    for(var i=0 ; i < b.length ;i++){
      if (b[i].checked == true){
        return b[i].value
      } 
    }
  }
/*
function main(){
  document.getElementById('loader').style.display='block';
  document.getElementById('aaa').style.display='none';
  setTimeout(main1,1000);
}
main();*/
var product_filter_response
var count=0;
var start=0;
var end=0;
var page_count=0
  function pagechange(btn){
    var val=document.getElementById('pagecount').value
    if (btn.getAttribute('id')=="privious_btn"){
      val=Number(val)-1;
      document.getElementById('pagecount').setAttribute('value',val);
      pagechangeprocess(val);
    }
    else{
      val=Number(val)+1;
      document.getElementById('pagecount').setAttribute('value',val);
      pagechangeprocess(val);
    }

  }

  function pagechangeprocess(val){
    console.log("Page Number -"+val)
    if (page_count <=1){
          start=0;
          end=count;
          document.getElementById('next_btn').disabled=true;
          document.getElementById('privious_btn').disabled=true;
    }
    else{

            if (val<=1){
              /*boundary condition to avoid if there is one two page
              for eg. if page_count=2 */
              document.getElementById('privious_btn').disabled=true;
              document.getElementById('next_btn').disabled=false;
              start=0
              end=12
              
            }
            else if(val >=page_count){
              start=val*12 -12
              end=count
              document.getElementById('next_btn').disabled=true;
              document.getElementById('privious_btn').disabled=false;
              
            }
            else{
              start=val*12 -12
              end=val*12
              document.getElementById('next_btn').disabled=false;
              document.getElementById('privious_btn').disabled=false;
            }
            
         }//console.log(start+ "-" + end)
      insert_into_productfilter();

  }

  function privious_btn_funtion(){
    if(Number(document.getElementById('pagecount').getAttribute('value')) == 1){
      document.getElementById('privious_btn').disabled=true;
    }
  }
privious_btn_funtion();

function page_change_function(count1){

      page_count=Math.ceil(count1/12);
      //console.log("number of pages >"+ page_count)
      if(page_count ==1){
        start=0;
        end=count
        document.getElementById('next_btn').disabled=true;
        document.getElementById('privious_btn').disabled=true;
      }
      else{
        //if number of pages is not equal to 1 enable next button;
        document.getElementById('next_btn').disabled=false;
      }
          
}

function insert_into_productfilter(){
  //console.log("length of response >"+product_filter_response['Info'].length);
  var response=product_filter_response
  var info="";
  var PopularLights = document.getElementById('Watchlist');
  if (response['Info'].length <1){
    PopularLights.innerHTML=info;
    return 1;
  }
  for(var i=start;i<end;i++){
    var save=response['Info'][i]['ProductPrice']-response['Info'][i]['DiscountPrice']

                        info=info+'<div class="col-sm-3 rounded " style="margin-top: 45px">\
                        <div class="Product_box shadow-sm" onmouseover="bigshadow(this)" onmouseout="normalshadow(this)" style="width:230px; ">\
                        <div class="product_image">\
                        <a href="#"><img src=../'+response['Info'][i]['ProductImageAddress']+' class="shadow-sm" style="width:230px;height: 200px;"></a></div><div class="product_information shadow"><div class="row" style=""><div class="col-sm" style="font-size: 14px;margin-left:10px"><p> <b>'+response['Info'][i]['ProductName']+'</b><br>'+response['Info'][i]['ProductType']+',led,'+response['Info'][i]['ProductType1']+','+response['Info'][i]['ProductSpecification']+'<br>        <b>Rs.<s style="color:gray;font-size:10px">'+response['Info'][i]['ProductPrice']+' </s>'+response['Info'][i]['DiscountPrice']+'<br><lable style="color:orange;font-size:12px">('+response['Info'][i]['DiscountRate']+'%)<label style="color:green"> Save Rs.'+save+'           </label></label></b>     </p></div></div><div class="row"><div class="col-sm" style="height: 50px;margin-left: 5px">\
                        <button class="btn btn-outline-danger btn-sm" style="width:100%;" value='+response['Info'][i]['ProductId']+' onclick="watchlist(this)"><b>WatchList</b></button></div><div class="col-sm" style="height: 50px;margin-right: 5px"><form method="post"><input type="hidden" name="ProductName" value='+response['Info'][i]['ProductId']+'><button class="btn btn-outline-success btn-sm" style="width:100%;" formtarget=”_blank”><b>See</b></button></form></div></div></div></div></div>'
                      }
                      PopularLights.innerHTML=info;
}

  

function main() {
  //loading all data
    ptype_checkbox=p_type_checkbox();
    pbrand_checkbox=brand_checkbox();
    pprice_checkbox=price_checkbox();
    pproduct_checkbox=product_checkbox();
    pwaranty_checkbox = p_warranty_checkbox();
    var obj={ptype:ptype_checkbox,pbrand :pbrand_checkbox,
      pproduct:pproduct_checkbox,pprice:pprice_checkbox.split('-'),pwarranty:pwaranty_checkbox}
  

    

  var url=localStorage.getItem("url");
  
  $.post(url+"get_customerproductfilter",{sql:JSON.stringify(obj)},
                
                function(response){
                  document.getElementById('numberofresult').innerHTML=response['Info'].length+'   Result Found';
                  var info="";
                  

            

                  //product page change part
                  
                  product_filter_response=response;
                  document.getElementById('pagecount').setAttribute('value','1');
                  start=0;end=12
                  count=response['Info'].length
                  page_change_function(response['Info'].length);
                  //product page change part end
                  console.log(start+ "-" + end)
                  insert_into_productfilter();
                

                  
          
              },"json");

}

main();
function bigshadow(x){
  x.setAttribute("class","Product_box shadow-lg");
}

function normalshadow(x){
  x.setAttribute("class","Product_box shadow-sm");
}








  

