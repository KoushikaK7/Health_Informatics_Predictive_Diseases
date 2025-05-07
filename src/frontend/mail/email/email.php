<?php

require_once 'phpgmailer/class.phpgmailer.php';

$mail = new PHPGMailer();   //object creation

$mail->Username = "shana.chammu@gmail.com"; //gmail
$mail->Password = "roshinipriya"; //gmail password
        					
$mail->From = "shana.chammu@gmail.com";   //from email id
$mail->FromName = "shana t"; //from name
$mail->Subject = "Test Subject"; //Subject of email
        					
$mail->AddAddress("shana.chammu@gmail.com");  //To email address
$mail->IsHTML(TRUE);  //If html content it is required

//Mailer content html
$content = "<html><head><title>Test Email</title></head>";
$content = $content."<body>";
$content = $content."<table width='100%'>";
$content = $content."<thead><tr><th>Employee ID</th><th>Employee Name</th><th>Employee Salary</th></tr></thead>";
$content = $content."<tbody><tr><td>1</td><td>ABC</td><td>150000</td></tr>";
$content = $content."<tr><td>2</td><td>XYZ</td><td>250000</td></tr></tbody>";
$content = $content."</table>";
$content = $content."</body>";
$content = $content."</html>";      					
$mail->Body = $content;
if(!$mail->Send())
{
   echo "Message could not be sent. <p>";
   echo "Mailer Error: " . $mail->ErrorInfo;
   exit;
}

echo "Message has been sent";
//$mail->Send();

?>