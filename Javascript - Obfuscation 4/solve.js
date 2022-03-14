var ð= "\x71\x11\x24\x59\x8d\x6d\x71\x11\x35\x16\x8c\x6d\x71\x0d\x39\x47\x1f\x36\xf1\x2f\x39\x36\x8e\x3c\x4b\x39\x35\x12\x87\x7c\xa3\x10\x74\x58\x16\xc7\x71\x56\x68\x51\x2c\x8c\x73\x45\x32\x5b\x8c\x2a\xf1\x2f\x3f\x57\x6e\x04\x3d\x16\x75\x67\x16\x4f\x6d\x1c\x6e\x40\x01\x36\x93\x59\x33\x56\x04\x3e\x7b\x3a\x70\x50\x16\x04\x3d\x18\x73\x37\xac\x24\xe1\x56\x62\x5b\x8c\x2a\xf1\x45\x7f\x86\x07\x3e\x63\x47";
function _(x,y)
{
	return x^y;
}
function __(y)
{
	var z = 0;
	for(var i=0;i<y;i++)
		{
			z += Math.pow(2,i);
		}
	return z;
}
function ___(y)
{
	var z = 0;
	for(var i=8-y;i<8;i++)
		{
			z += Math.pow(2,i);
		}
	return z
}
function ____(x,y)
{
	y = y % 8;
	Ï = __(y);
	Ï = (x & Ï) << (8-y);
	return (Ï) + (x >> y);
}
function _____(x,y)
{
	y = y % 8;
	Ï = ___(y);
	Ï = (x & Ï) >> (8-y);
	return ((Ï) + (x << y)) & 0x00ff;
}
function ______(x,y)
{
	return _____(x,y)
}
function _______(_________,key)
{
	________ = "";
	________2 = "";
	for(var i=0;i<_________.length;i++)
		{
			c = _________.charCodeAt(i);
			if(i != 0)
				{
					t = ________.charCodeAt(i-1)%2;
					switch(t)
					{
						case 0:
						cr = _(c, key.charCodeAt(i % key.length));
						break;
						case 1:
						cr = ______(c, key.charCodeAt(i % key.length));
						break;
					}
				}
			else
				{
					cr = _(c, key.charCodeAt(i % key.length));
				}
					________ += String.fromCharCode(cr);
			}
		return ________;
}
function __________(þ)
{
	var ŋ=0;
	for(var i=0;i<þ.length;i++)
		{
			ŋ+=þ["charCodeAt"](i)
		}
		if(ŋ==8932)
		{
				return true
		}
		else
		{
			return false;
		}
}
//__________(_______(ð,prompt("Mot de passe?")));

var char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-=~!@#$%^&*()_+[]\{}|;':\",./<>?";
var result = '<html>'
var s1=''

function check_same(x,y,k)
{
	for(var i=0; i <= k; i++)
	{
		if(x[i] !== y[i])
			return false;
	}
	return true;
}


var s3=[]
var s2 = []
for(var i=0; i< 6; i++)
{
	s3 = []
	if (s2.length == 0)
	{
		for(var j=0; j < char_set.length; j++)
		{
			X = _______(ð, char_set[j]);
    		if(X != void(0) && X.length >= i+1)
        		if(check_same(result,X,i)==true)
        		{
        			s3.push(char_set[j])
        		}
        	}
		}
	else{

		for(var k=0; k <= s2.length; k++ )
		{
			for(var j=0; j < char_set.length; j++)
			{
				X = _______(ð, s2[k] + char_set[j]);
    			if(X != void(0))
        			if(check_same(result,X,i)==true)
        			{
        				s3.push(s2[k] + char_set[j])
        			}
        	}
    	}
    }
    console.log(s3)
    s2=s3
}
for (var i = 0; i< s2.length; i++){
	if(__________(_______(ð,s2[i])))
		console.log(s2[i]);
}
