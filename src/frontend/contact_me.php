<script>
console.log("hi");

</script>
<?php

#
#$name = $_POST['name'];
#$email_address = $_POST['email'];
#$phone = $_POST['phone'];
#$message = $_POST['message'];
#$to = 'koushika26k7@gmail.com';
#$subject = "HTML email";
// Always set content-type when sending HTML email
#$headers = "MIME-Version: 1.0" . "\r\n";
#$headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";

// More headers
#$headers .= 'From: <koushika26k7@gmail.com>' . "\r\n";
#$headers .= 'Cc: koushika26k7@gmail.com' . "\r\n";

// Please specify your Mail Server - Example: mail.example.com.
#ini_set("SMTP","tls://smtp.gmail.com");

// Please specify an SMTP Number 25 and 8889 are valid SMTP Ports.
#ini_set("smtp_port","465");

// Please specify the return address to use
#ini_set('sendmail_from', 'kauhika26k7@gmail.com');

#mail($to,$subject,$message,$headers);
#RETURN true;
#
require_once 'phpgmailer/class.phpgmailer.php';

$mail = new PHPGMailer();   //object creation

// Check for empty fields
   

$name = $_POST['name'];
$email_address = $_POST['email'];
$phone = $_POST['phone'];
$message = $_POST['message'];

#echo phpinfo();  
#if(empty($_POST['name'])      || empty($_POST['email'])     || empty($_POST['phone'])     || empty($_POST['message'])   ||!filter_var($_POST['email'],FILTER_VALIDATE_EMAIL))
#   {
#   echo "No arguments Provided!";
 #  return false;
#   }

ini_set("SMTP","ssl://smtp.gmail.com");
ini_set("smtp_port","465");

// Create the email and send the message
$to = 'koushika26k7@gmail.com'; // Add your email address inbetween the '' replacing yourname@yourdomain.com - This is where the form will send a message to.
$email_subject = "Website Contact Form:  $name";
$email_body = "You have received a new message from your website contact form.\n\n"."Here are the details:\n\nName: $name\n\nEmail: $email_address\n\nPhone: $phone\n\nMessage:\n$message";
$headers = "From: noreply@yourdomain.com\n"; // This is the email address the generated message will be from. We recommend using something like noreply@yourdomain.com.
$headers .= "Reply-To: $email_address";   
$res=mail($to,$email_subject,$email_body,$headers);
echo $res;
return true;         
?>