# pb_bp_ue
This is a tools for associating proto with ue-blueprint 


# build
## linux
```
 cd  preject_dir/
pip install pyinstaller
python -m venv  bpvenv
pip install -r requirements.txt
pyinstaller -F --name=pb_ue ./src/main.py
```
# run
```
// parameters : proto_dir  tmpl_directPath  gen_cpp_dir
 cd dist
 ./pb_ue ../proto/ ../tmpls/ ../cpps/
 //noted: the  gen_cpp_dir  shuold be exist
```

# Note
## request  body & request msg id
 ProtoMsgId.proto:
```
  ACCOUNT_LOGIN_REQ = 10;// req=AccountLoginReq,desc="此消息是客户端sdk 登录完后 进入游戏的login 服务器 进行账号登录"
  ACCOUNT_LOGIN_RES = 11;//res=AccountLoginRes, desc="登录完返回消息"
```
##  error  code 
 ProtoErrorCode.proto:
```
  INVALID_LOGIN_TOKEN = 3;//玩家 token 不合法
  INVALID_PARAM = 10; //入参 不合法
```

 .proto file format samples
 ## comment
   should be as left-right:
```
  bool require_password = 1; // 是否需要重发带密码的请求 
```
  do not as above-below it will be removed:
```
 // 是否需要重发带密码的请求  this will be lost
  bool require_password = 1;
```
    