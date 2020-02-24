function Description(key,value,somevalue) {
    var self = this;
    (key === undefined) ? key = '' : key = key;
    (value === undefined) ? value = '' : value = value; 
    self.key1 = ko.observable(key); 
    self.value1 = ko.observable(value);  
    self.isEnableX = function(value){
    return somevalue;
    } 
}
function Group(name,p,des,somevalue) {
    var self = this;
    (name === undefined) ? name = '' : name = name; 
    (p === undefined) ? p = '' : p = p; 
    self.gname = ko.observable(name); 
    self.gp = ko.observable(p);
    self.desc = ko.observableArray([]);
    for (var prop in des) {
      self.desc.push(new Description(prop,des[prop],true));
    }
    self.keyError = ko.observable(false);
    self.mangroupError = ko.observable(false);
    self.addDesc = function(des) {
      if (self.gname() != "" && self.gp() != "" ){
        if(self.desc()=='' || self.desc()[self.desc().length-1].key1()!="" && self.desc()[self.desc().length-1].value1()!=""){
        self.desc.push(new Description());
        self.keyError(false);
        self.mangroupError(false);
      }
      else{
        self.keyError(true);
      }
      }
      else {
        self.mangroupError(true);
      }
    }
    self.isEnableX = function(value){
    return somevalue;
    }
}


function varientInput(name){
  var self = this;
  self.varientText = ko.observable(name);
  self.quantityValue = ko.observable("");
}

function FormViewModel() {
  var self = this;
  self.productId = ko.observable(null);
  self.productName = ko.observable("false");
  self.id = ko.observable(self.productId);
  self.categories = ko.observableArray({{category|safe}});
  self.selectedCat = ko.observable();
  self.name = ko.observable("");
  self.price = ko.observable("");
  self.varient = ko.observable("no");
  self.wholesale = ko.observable();
  var vquant = [];
  self.vQuantity = ko.observable();
  self.quantity = ko.computed(function(value){
    if (self.varient() == "no"){
      return value;
    }
    else {
      var sum = 0;
      for (var i = 0;i < self.textFields().length;i++)
        sum =  sum + parseInt(self.textFields()[i].quantityValue());
        return sum;
    }
  });
  self.desc = ko.observable("");
  self.discount = ko.observable("");
  self.discountType = ko.observable("percentage");
  
  self.varientsField = ko.computed(function(){
    return self.varient() == "yes";
  });      
   // ko.observable(self.varient()=='yes');
  self.varientValuesJunk = ko.observable("");
  self.varientValues = ko.computed(function(){
    var x =  $.trim(self.varientValuesJunk()).split(/\s*\,\s*/);
    return x.filter(function(n){ return n != "" }); 
  });

  self.textFields = ko.observableArray([])
  self.makeTextBox = function(){
    self.textFields([]);
    for(var i=0;i < self.varientValues().length; i++){
      self.textFields.push(new varientInput(self.varientValues()[i]));
    }
  }
  self.varientValue = ko.observable("");
  self.is_wholesale = ko.observable(false);
  self.isreqprice = ko.observable(true);
  self.fileContainer = ko.observable(false);
  self.formContainer = ko.observable(true);
  self.formError = ko.observable(false);
  var errorOnProductForm = false;
  self.varientName = ko.observable("")
  var errorOnForm = false;
  self.saveall = function () {
    self.formError(false);
    for (var i=0;i< self.group().length;i++){
      for (var j=0;j< self.group()[i].desc().length;j++){
        if((self.group()[i].desc()[j].key1()=='' && self.group()[i].desc()[j].value1()!='') ||
          (self.group()[i].desc()[j].key1()!='' && self.group()[i].desc()[j].value1()=='')){
          errorOnForm = true;
        }
      }
    }
    if (!errorOnForm){
       $.post(
      "/add-product-details/",
     {'csrfmiddlewaretoken' : "{{csrf_token}}",
      'data': ko.toJSON(self.group())
      // 'discount':self.discount,
      }, 
     function (data) {
        if (data.success) {
        }
      });
    }
    else {
      self.formError(true);
      errorOnForm = false;
    }
  }
  var des1 = {"color":"red",
      "fabric":"cotton",
  };
  var des2 = {
      "SKUNO":"334HU43"
  };
  self.group = ko.observableArray();
  self.groupError = ko.observable(false);
  self.addGroup = function(des) {
        if(self.group()=='' || self.group()[self.group().length-1].gname()!="" && self.group()[self.group().length-1].gp()!=""){
          (self.group().length == 0)? self.group.push(new Group("Hightlights","1")):self.group.push(new Group());
          self.groupError(false)
        }
        else{
            self.groupError(true);
        }
  } 

  self.myAction = function(){
    if(self.is_wholesale()==true){
      self.wholesale(self.price());
      self.isreqprice(false);
    }
    else {
       self.wholesale("");
       self.isreqprice(true);
      }
    return true;
    };

    self.open_modal_upload_image = function(){     
      $.post(
      "/add-product-post/",
     {'csrfmiddlewaretoken' : "{{csrf_token}}",
      'name':self.name,
      'price':self.price,
      'wholesale_price':self.wholesale,
      'quantity':self.quantity,
      'desc':self.desc,
      'category':self.selectedCat,
      'varient':ko.toJSON(self.textFields()),
      'varientname':self.varientName()
      // 'discount':self.discount,
      }, 
     function (data) {
        if (data.success) {
          self.productId = data.productId;
          self.id(self.productId);
          $('#formCont').fadeOut();
          $('#uploadCont').fadeIn();
          self.fileContainer(true);
          self.productName(self.name());
          des = data.data
          for(var i = 0, size = des.length; i < size ; i++){
            var item = des[i];
            self.group.push(new Group(item['name'],item['priority'],item['keys'],true))
          }
        }
      });
      
    }
  };

ko.applyBindings(new FormViewModel());