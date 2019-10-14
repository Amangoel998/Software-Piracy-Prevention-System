def _generate_jwt_token(self, idg, soft):
        """ Generate Tokens """
        dt = datetime.now() + timedelta(days=365)
        token = jwt.encode({
            'user_id': idg,
            'exp': int(dt.strftime('%s'))

        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')