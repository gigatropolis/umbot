
set GOOS=linux
set GOARC=amd64
go build beersrv.go
cp beersvr.exe bin\beersvr_linux_amd64

set GOOS=linux
set GOARC=amd64
go build beersrv.go
cp beersvr bin\beersvr_linux_amd64

set GOOS=linux
set GOARC=386
go build beersrv.go
cp beersvr bin\beersvr_linux_386

set GOOS=linux
set GOARC=arm
go build beersrv.go
cp beersvr bin\beersvr_linux_arm

set GOOS=darwin
set GOARC=arm64
go build beersrv.go
cp beersvr bin\beersvr_darwin_amd64

