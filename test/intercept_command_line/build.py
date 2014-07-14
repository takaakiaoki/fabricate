#!/usr/bin/env python

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../../')
    import fabricate

    default='myfab'
    
    def myfab():
        fabricate.run('touch', 'testfile')
    
    def clean():
        fabricate.autoclean()
    
    if len(sys.argv) > 1:
        default=sys.argv[1]
    
    fabricate.main(command_line=[default])
