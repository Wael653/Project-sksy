  cl_data = super().clean()

        vorname = cl_data.get('vorname').strip()
        nachname = cl_data.get('nachname').strip()
        from_email = cl_data.get('email')
        betreff = cl_data.get('betreff')
        msg = render_to_string('email_support.html', {'name': betreff,'email': from_email, 'message': cl_data.get('nachricht')})
        plain_msg = strip_tags(msg)
        msg = msg.replace("\r\n", "<br>")
        return betreff, msg, plain_msg, from_email

    def send(self):

        betreff, msg, plain_msg, from_email  = self.get_info()

        send_mail(
            betreff,
            plain_msg,
            from_email,
            [from_email],
            html_message= msg
        )