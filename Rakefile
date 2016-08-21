require 'pathname'
DATA_DIR = Pathname 'data'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR. / 'corral'
SCRIPTS_DIR = WRANGLE_DIR / 'scripts'
DIRS = {
    :fetched => CORRAL_DIR / ('fetched'),
    :compiled => CORRAL_DIR / ('compiled'),
    :published => DATA_DIR,
}




P_FILES = Hash[{

    fips: 'fips.csv',

}.map{|k, v| [k, DATA_DIR / v ] }]



desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        p.mkpath()
        puts "Created directory: #{p}"
    end
end

desc 'counties extracted'
fn = DIRS[:compiled].join('counties-unemployment.csv')
file fn do
    sh ["python",
            SCRIPTS_DIR / 'extract_county_unemployment.py',
            DIRS[:fetched] / 'la.data.64.County',
            '>', fn].join(" ")
end


desc "Fetch FIPS lookups from BLS"
file P_FILES[:fips] do
    sh ["python",
            SCRIPTS_DIR / 'fetch_fips.py',
            '>', P_FILES[:fips]].join(" ")
end




