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

  grunt.registerTask('local', ['bgShell:runServer']);
  grunt.registerTask('production', []);
  grunt.registerTask('default', ['production']);
};
