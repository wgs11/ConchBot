def incrementcolor(color, value):
        file = color+'.txt'
        f = open(file,'r+')
        total = int(f.read())
        total = total + int(value)
        f.seek(0)
        f.write(str(total))
        f.truncate()
        f.close