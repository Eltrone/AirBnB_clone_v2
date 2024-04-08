file { '/data':
  ensure => directory,
}

file { '/data/web_static':
  ensure => directory,
}

file { '/data/web_static/releases':
  ensure => directory,
}

file { '/data/web_static/shared':
  ensure => directory,
}

file { '/data/web_static/releases/test':
  ensure => directory,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,  # Ceci permet de remplacer le lien s'il existe déjà
}

File['/data/web_static',
     '/data/web_static/releases',
     '/data/web_static/shared',
     '/data/web_static/releases/test',
     '/data/web_static/releases/test/index.html',
     '/data/web_static/current'] -> {
  owner  => 'ubuntu',
  group  => 'ubuntu',
}
