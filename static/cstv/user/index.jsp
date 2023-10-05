<%@page contentType="text/html; charset=utf-8" language="java"
import="java.io.BufferedReader"
import="java.io.InputStream"
import="java.io.InputStreamReader"
import="java.io.OutputStream"
import="java.util.Enumeration"
import="java.io.OutputStreamWriter"
import="java.net.HttpURLConnection"
import="java.net.URL"
import="java.io.Writer"
%><%!
void doIn (HttpURLConnection conn,HttpServletRequest request) throws Exception{
	conn.setRequestMethod("POST");
	conn.setDoOutput(true);

	InputStream post=request.getInputStream();
			
	
	conn.setRequestProperty("Accept","text/html, */*; q=0.01");
	conn.setRequestProperty("Cookie",request.getHeader("Cookie"));
	conn.setRequestProperty("Content-Type",request.getHeader("Content-Type"));
	
	OutputStream os=conn.getOutputStream();
	
	while(true){
		int i=post.read();
		if(i!=-1){
			os.write(i);
		}else{
			break;
		}
	}
	os.flush();
	os.close();
}
void doOut(HttpURLConnection conn,HttpServletResponse response) throws Exception {
	InputStream in= conn.getInputStream();
	Writer out=response.getWriter();

	BufferedReader br =new BufferedReader(new InputStreamReader(in,"utf-8"));
	while(true){
		String line=br.readLine();
		if(line==null){
			break;
		}else{
			out.write(line);
		}
	}
	br.close();
}
%><%
URL url=new URL("http://60.206.137.156:8020/video_api/user/channelList/c196266f837d14e0b693f961bee37b66");
HttpURLConnection conn=(HttpURLConnection) url.openConnection();
doIn(conn,request);
doOut(conn,response);




%>