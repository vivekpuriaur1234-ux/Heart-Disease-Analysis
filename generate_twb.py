import os

def create_tableau_twb(filename, csv_path):
    abs_csv_path = os.path.abspath(csv_path)
    
    twb_content = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook original-version='18.1' source-build='2023.1.0' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <AutoLayoutByNesting />
    <DashboardLayoutElementSpecificMeasures />
    <DashboardLayoutOptimized />
    <DashboardsByNesting />
    <Thumbnail />
  </document-format-change-manifest>
  <style />
  <datasources>
    <datasource caption='housing_data' inline='true' name='federated.housing_data' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='housing_data' name='textscan.housing_data'>
            <connection class='textscan' directory='{os.path.dirname(abs_csv_path)}' filename='{os.path.basename(abs_csv_path)}' password='' server='' />
          </named-connection>
        </named-connections>
      </connection>
      <column datatype='integer' name='[Sale_Price]' role='measure' type='quantitative' />
      <column datatype='integer' name='[Flat Area (in Sqft)]' role='measure' type='quantitative' />
      <column datatype='integer' name='[Overall Grade]' role='dimension' type='quantitative' />
      <column datatype='integer' name='[No of Bedrooms]' role='dimension' type='quantitative' />
      <column datatype='integer' name='[Basement Area (in Sqft)]' role='measure' type='quantitative' />
      <layout dim-ordering='alphabetic' measure-ordering='alphabetic' show-structure='true' />
      <semantic-values>
        <semantic-value key='[Country].[Name]' value='&quot;United States&quot;' />
      </semantic-values>
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='Price_vs_Area_Scatter'>
      <table>
        <view>
          <datasources>
            <datasource caption='housing_data' name='federated.housing_data' />
          </datasources>
          <datasource-dependencies datasource='federated.housing_data'>
            <column datatype='integer' name='[Sale_Price]' role='measure' type='quantitative' />
            <column datatype='integer' name='[Flat Area (in Sqft)]' role='measure' type='quantitative' />
            <column-instance column='[Sale_Price]' derivation='Sum' name='[sum:Sale_Price:qk]' pivot='key' type='quantitative' />
            <column-instance column='[Flat Area (in Sqft)]' derivation='Sum' name='[sum:Flat Area (in Sqft):qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Automatic' />
          </pane>
        </panes>
        <rows>[federated.housing_data].[sum:Sale_Price:qk]</rows>
        <cols>[federated.housing_data].[sum:Flat Area (in Sqft):qk]</cols>
      </table>
    </worksheet>
    <worksheet name='Grade_Distribution_Bar'>
      <table>
        <view>
          <datasources>
            <datasource caption='housing_data' name='federated.housing_data' />
          </datasources>
          <datasource-dependencies datasource='federated.housing_data'>
            <column datatype='integer' name='[Overall Grade]' role='dimension' type='quantitative' />
            <column-instance column='[Overall Grade]' derivation='Count' name='[cnt:Overall Grade:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.housing_data].[cnt:Overall Grade:qk]</rows>
        <cols>[federated.housing_data].[Overall Grade]</cols>
      </table>
    </worksheet>
    <worksheet name='Bedrooms_Box_Plot'>
      <table>
        <view>
          <datasources>
            <datasource caption='housing_data' name='federated.housing_data' />
          </datasources>
          <datasource-dependencies datasource='federated.housing_data'>
            <column datatype='integer' name='[No of Bedrooms]' role='dimension' type='quantitative' />
            <column datatype='integer' name='[Sale_Price]' role='measure' type='quantitative' />
            <column-instance column='[Sale_Price]' derivation='Sum' name='[sum:Sale_Price:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Automatic' />
          </pane>
        </panes>
        <rows>[federated.housing_data].[sum:Sale_Price:qk]</rows>
        <cols>[federated.housing_data].[No of Bedrooms]</cols>
      </table>
    </worksheet>
  </worksheets>
  <dashboards>
    <dashboard name='Housing_Market_Insights'>
      <style />
      <size maxheight='900' maxwidth='1200' minheight='900' minwidth='1200' />
      <zones>
        <zone h='100000' id='4' type-static='layout-basic' w='100000' x='0' y='0'>
          <zone h='50000' id='5' name='Price_vs_Area_Scatter' type-static='worksheet' w='60000' x='0' y='0' />
          <zone h='50000' id='6' name='Grade_Distribution_Bar' type-static='worksheet' w='40000' x='60000' y='0' />
          <zone h='50000' id='7' name='Bedrooms_Box_Plot' type-static='worksheet' w='100000' x='0' y='50000' />
        </zone>
      </zones>
    </dashboard>
  </dashboards>
  <windows>
    <window class='dashboard' name='Housing_Market_Insights'>
      <viewpoints />
      <active id='-1' />
    </window>
  </windows>
</workbook>
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(twb_content)
    print(f"Tableau workbook generated at {filename}")

if __name__ == "__main__":
    create_tableau_twb("tableau/housing_dashboard.twb", "dataset/housing_data.csv")
