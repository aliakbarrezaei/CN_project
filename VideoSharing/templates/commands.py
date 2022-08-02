def account_urls():
    cmds = ['/accounts/login/',
            '/accounts/register/',
            '/accounts/logout/', ]
    return [(cmd + '<br>') for cmd in cmds]


def ticketing_urls():
    cmds = ['/tickets/my/',
            '/tickets/my/new/',
            ' ',
            '/tickets/users/',
            '/tickets/users/all/',
            '/tickets/users/{id}/assign/',
            '/tickets/users/{id}/edit/', ]

    return [(cmd + '<br>') for cmd in cmds]


# ----------------------------------------------
def user_commands():
    cmds = ['user_login/',
            'user_register/',
            'user_logout/',
            'my_tickets/',
            'my_tickets/new/']

    return [('\n<li>' + cmd + '</li>') for cmd in cmds]


def admin_commands():
    cmds = ['user_login/'
            'user_register/',
            'user_logout/',
            'my_tickets/',
            'my_tickets/new/']
    return [('\n<li>' + cmd + '</li>') for cmd in cmds]


