module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    bgShell: {
      runServer: {
        bg: false,
        cmd: 'python <%= pkg.name %>/manage.py runserver'
      }
    }
  });

  grunt.registerTask('build', []);
  grunt.registerTask('run', ['bgShell:runServer']);
  grunt.registerTask('deploy', []);
  grunt.registerTask('default', ['build', 'run']);
};
